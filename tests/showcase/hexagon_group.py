from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.matrices import *
from raytracer.scene import World
from raytracer.shapes import *
from raytracer.tuples import Color, Point, Vector


def hexagon_corner():
    corner = Sphere()
    corner.transformation = translation(0, 0, -1) * scaling(0.25, 0.25, 0.25)
    return corner


def hexagon_edge():
    edge = Cylinder()
    edge.minimum = 0
    edge.maximum = 1
    edge.transformation = translation(0, 0, -1) * rotation_y(-pi / 6) * \
        rotation_z(-pi / 2) * scaling(0.25, 1, 0.25)
    return edge


def hexagon_side():
    side = Group()
    side.add_children(hexagon_corner(), hexagon_edge())
    return side


def hexagon():
    _hex = Group()
    for n in range(6):
        side = hexagon_side()
        side.transformation = rotation_y(n * pi / 3)
        _hex.add_children(side)
    _hex.transformation = rotation_x(-pi / 6) * translation(0, 1, 0)
    return _hex


if __name__ == '__main__':
    world = World()
    world.add(hexagon())
    world.light_source = PointLight(Point(-5, 5, -5), Color.white())

    camera = Camera(160, 120, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -10), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}hexagon.ppm')
