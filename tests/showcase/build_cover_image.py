from copy import copy
from os import sep
from yaml import load
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.matrices import *
from raytracer.scene import World
from raytracer.shapes import *
from raytracer.tuples import *

import pprint
import raytracer

constants = {}


def point_from_tuple(_tuple):
    return Tuple.create_from(*_tuple, 1)


def vector_from_tuple(_tuple):
    return Tuple.create_from(*_tuple, 0)


def build_camera(_data: dict) -> Camera:
    _camera = Camera(_data['width'], _data['height'], _data['field-of-view'])
    _camera.transformation = view_transform(point_from_tuple(_data['from']),
                                            point_from_tuple(_data['to']),
                                            vector_from_tuple(_data['up']))
    return _camera


def build_light(_data: dict) -> PointLight:
    return PointLight(point_from_tuple(_data['at']), Color(*_data['intensity']))


def build_material(_data: dict) -> Material:
    if 'extend' not in _data:
        material = Material()
    else:
        material = copy(constants[_data['extend']])
    for key, value in _data['value'].items():
        if key != 'color':
            setattr(material, key, value)
        else:
            setattr(material, key, Color(*value))
    return material


def build_transformation(_data: dict, key: str) -> Matrix:
    tr = Matrix.identity()
    for step in _data[key]:
        if isinstance(step, str) and step in constants:
            tr *= constants[step]
        else:
            tr = getattr(tr, step[0].replace('-', '_'))(*step[1:])
    return tr


def build_shape(_data: dict) -> Shape:
    class_name = getattr(raytracer.shapes, _data['add'].capitalize())
    shape = class_name()

    shape.transformation = build_transformation(_data, 'transform')
    if isinstance(_data['material'], str):
        shape.material = constants[_data['material']]
    else:
        shape.material = build_material({'value': _data['material']})
    return shape


if __name__ == '__main__':
    with open(f'..{sep}resources{sep}cover.yaml') as f:
        data = load(f)
        pprint.pprint(data)

    camera = build_camera(data[0])

    world = World()
    world.light_source = build_light(data[1])

    # skip second light source... raytracer doesn't implement this yet

    for element in data[3:]:
        if 'define' in element:
            if element['define'].endswith('material'):
                constants[element['define']] = build_material(element)
            else:
                constants[element['define']] = build_transformation(element, 'value')
        else:
            world.add(build_shape(element))

    # print('Parsed constants:')
    # pprint.pprint(constants)
    #
    # print('World object:')
    # pprint.pprint(world.objects)

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}book_cover.ppm')

