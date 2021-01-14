from math import pi
from os import sep
from raytracer.camera import Camera
from raytracer.canvas import write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.matrices import scaling, rotation_y, rotation_x, translation, view_transform
from raytracer.scene import World
from raytracer.shapes import Sphere, Plane
from raytracer.tuples import Color, Point, Vector


if __name__ == '__main__':
    floor = Plane()
    floor.material = Material()
    floor.material.color = Color(1, 0.9, 0.9)
    floor.material.specular = 0

    middle = Sphere()
    middle.transformation = translation(-0.5, 1, 0.5)
    middle.material = Material()
    middle.material.color = Color(0.5, 0, 0)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.reflective = 1

    right = Sphere()
    right.transformation = translation(1.5, 0.5, -0.5) * scaling(0.5, 0.5, 0.5)
    right.material = Material()
    right.material.color = Color(0.2, 0.2, 0.8)
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    right.material.reflective = .5

    left = Sphere()
    left.transformation = translation(-1.5, 0.33, -0.75) * scaling(0.33, 0.33, 0.33)
    left.material = Material()
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3

    world = World()
    world.add(floor, middle, left, right)
    world.light_source = PointLight(Point(-10, 10, -10), Color.white())

    camera = Camera(240, 120, pi / 3)
    camera.transformation = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

    canvas = camera.render(world)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}reflective.ppm')
