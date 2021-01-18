from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.patterns import *
from raytracer.matrices import scaling, rotation_y, rotation_x, translation, view_transform
from raytracer.scene import World
from raytracer.shapes import Sphere, Plane
from raytracer.tuples import Color, Point, Vector


if __name__ == '__main__':
    floor = Plane()
    floor.material.color = Color(.1, 1, .1)
    floor.material.reflective = 0.9
    floor.material.transparency = 1
    floor.material.refractive_index = 1.333

    under = Sphere()
    under.transformation = translation(0, -.5, 0) * scaling(.25, .25, .25)
    under.material.color = Color(0, .8, 0)
    under.material.refractive_index = 1.5
    under.material.ambient = .8

    above = Sphere()
    above.transformation = translation(1, .5, 0) * scaling(.5, .5, .5)
    above.material.color = Color(.2, 0, 0)
    above.material.diffuse = .8
    above.material.ambient = .5

    bottom = Plane()
    bottom.transformation = translation(0, -1.25, 0)
    bottom.material.pattern = StripePattern(Color.black(), Color(0, .2, .2))
    bottom.material.diffuse = .25
    bottom.material.ambient = .25

    world = World()
    world.add(floor, under, above, bottom)
    world.light_source = PointLight(Point(-10, 10, -10), Color.white())

    camera = Camera(300, 200, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}reflect_refract.ppm')
