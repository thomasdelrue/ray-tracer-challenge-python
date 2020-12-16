from .intersections import Intersection, Intersections
from .rays import Ray
from .tuples import Point, Vector, dot
import math


class Sphere:
    def __init__(self):
        self.origin = Point(0, 0, 0)

    def intersect(self, ray: Ray):
        sphere_to_ray: Vector = ray.origin - self.origin

        a = dot(ray.direction, ray.direction)
        b = 2 * dot(ray.direction, sphere_to_ray)
        c = dot(sphere_to_ray, sphere_to_ray) - 1

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return Intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))

    def __repr__(self):
        return f'Sphere(origin={self.origin})'




