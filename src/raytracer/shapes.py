from abc import ABC, abstractmethod
from . import EPSILON
from .intersections import Intersection, Intersections
from .materials import Material
from .matrices import Matrix
from .rays import Ray
from .tuples import Point, Vector, dot
import math


class Shape(ABC):
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self.transformation = Matrix.identity()
        self.material = Material()

    def intersect(self, ray: Ray) -> Intersections:
        local_ray = ray.transform(self.transformation.inverse())
        return self._local_intersect(local_ray)

    @abstractmethod
    def _local_intersect(self, ray: Ray):
        ...

    def normal_at(self, point: Point) -> Vector:
        local_point = self.transformation.inverse() * point
        local_normal = self._local_normal_at(local_point)
        world_x, world_y, world_z, _ = self.transformation.inverse().transpose() * local_normal
        return Vector(world_x, world_y, world_z).normalize()

    @abstractmethod
    def _local_normal_at(self, point: Point) -> Vector:
        ...


class Sphere(Shape):
    def __init__(self):
        super().__init__()

    def _local_intersect(self, ray: Ray) -> Intersections:
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

    def _local_normal_at(self, point: Point) -> Vector:
        return point - self.origin

    def __repr__(self):
        return f'Sphere(origin={self.origin})'


class Plane(Shape):
    def _local_intersect(self, ray: Ray) -> Intersections:
        if abs(ray.direction.y) < EPSILON:
            return Intersections()
        t = -ray.origin.y / ray.direction.y
        return Intersections(Intersection(t, self))

    def _local_normal_at(self, point: Point) -> Vector:
        return Vector(0, 1, 0)
