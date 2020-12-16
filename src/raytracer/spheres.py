from .intersections import Intersection, Intersections
from .matrices import Matrix
from .rays import Ray
from .tuples import Point, Vector, dot
import math


class Sphere:
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self._transformation = Matrix.identity()

    def intersect(self, ray: Ray):
        tr_ray = ray.transform(self._transformation.inverse())
        sphere_to_ray: Vector = tr_ray.origin - self.origin

        a = dot(tr_ray.direction, tr_ray.direction)
        b = 2 * dot(tr_ray.direction, sphere_to_ray)
        c = dot(sphere_to_ray, sphere_to_ray) - 1

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return Intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def __repr__(self):
        return f'Sphere(origin={self.origin})'




