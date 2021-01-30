from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.patterns import *
from raytracer.matrices import translation, view_transform
from raytracer.scene import World
from raytracer.shapes import Cone
from raytracer.tuples import Color, Point, Vector


if __name__ == '__main__':
    # floor = Plane()
    # floor.material.color = Color(.8, .8, .8)
    # floor.material.reflective = .2

    cone = Cone(closed=False)
    cone.maximum = 1
    cone.minimum = -1
    cone.material.color = Color(.8, 0, 0)
    cone.material.reflective = .6
    cone.transformation = translation(0, 1, 0)

    world = World()
    world.add(cone)
    world.light_source = PointLight(Point(-5, 5, -5), Color.white())

    camera = Camera(160, 120, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}cone.ppm')
