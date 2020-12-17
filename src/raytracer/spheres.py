from .intersections import Intersection, Intersections
from .materials import Material
from .matrices import Matrix
from .rays import Ray
from .tuples import Point, Vector, dot
import math


class Sphere:
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self.transformation = Matrix.identity()
        self.material = Material()

    def intersect(self, ray: Ray):
        tr_ray = ray.transform(self.transformation.inverse())
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

    def normal_at(self, point: Point):
        object_point = self.transformation.inverse() * point
        object_normal = object_point - self.origin
        x, y, z, _ = self.transformation.inverse().transpose() * object_normal
        return Vector(x, y, z).normalize()

    def __repr__(self):
        return f'Sphere(origin={self.origin})'




