from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.matrices import *
from raytracer.scene import World
from raytracer.shapes import *
from raytracer.tuples import Color, Point, Vector


def triangle():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    t.material.color = Color(1, 0, 0)
    return t


if __name__ == '__main__':
    world = World()
    world.add(triangle())
    world.light_source = PointLight(Point(-5, 5, -5), Color.white())

    camera = Camera(160, 120, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -10), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}triangle.ppm')
