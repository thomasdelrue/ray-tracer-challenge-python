from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.matrices import *
from raytracer.patterns import GradientPattern
from raytracer.scene import World
from raytracer.shapes import *
from raytracer.tuples import Color, Point, Vector


def csg():
    s1 = Sphere()
    s1.transformation = translation(-0.375, 0, 0)
    s1.material.color = Color(1, 0, 0)
    s1.material.transparency = .8
    s2 = Sphere()
    s2.transformation = translation(0.375, 0, 0)
    s2.material.pattern = GradientPattern(Color(1, 0, 0), Color(1, 1, 0))
    s2.material.reflective = .8
    s2.material.transparency = .8
    c = Csg(OperationType.INTERSECTION, s1, s2)
    c.transformation = scaling(1, 1.5, 1) * rotation_y(-pi / 4)
    return c


if __name__ == '__main__':
    world = World()
    world.add(csg())
    world.light_source = PointLight(Point(-5, 5, -5), Color.white())

    camera = Camera(300, 200, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -10), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}csg.ppm')
