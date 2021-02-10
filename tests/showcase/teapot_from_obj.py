from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.matrices import *
from raytracer.obj_file import parse_obj_file
from raytracer.scene import World
from raytracer.tuples import Color, Point, Vector


def teapot():
    parser = parse_obj_file(f'..{sep}resources{sep}Sting-Sword-lowpoly.obj')
    return parser.obj_to_group()


if __name__ == '__main__':
    world = World()
    world.add(teapot())
    world.light_source = PointLight(Point(-5, 5, -5), Color.white())

    camera = Camera(150, 100, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -10), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}sting.ppm')
