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
    def _local_intersect(self, ray: Ray) -> Intersections:
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
        return f'Sphere(origin={self.origin} ref={self.material.refractive_index})'


class Plane(Shape):
    def _local_intersect(self, ray: Ray) -> Intersections:
        if abs(ray.direction.y) < EPSILON:
            return Intersections()
        t = -ray.origin.y / ray.direction.y
        return Intersections(Intersection(t, self))

    def _local_normal_at(self, point: Point) -> Vector:
        return Vector(0, 1, 0)


def _check_axis(origin: float, direction: float) -> (float, float):
    t_min_numerator = -1 - origin
    t_max_numerator = 1 - origin

    if abs(direction) >= EPSILON:
        t_min = t_min_numerator / direction
        t_max = t_max_numerator / direction
    else:
        t_min = t_min_numerator * float('inf')
        t_max = t_max_numerator * float('inf')

    if t_min > t_max:
        t_min, t_max = t_max, t_min

    return t_min, t_max


class Cube(Shape):
    def _local_normal_at(self, point: Point) -> Vector:
        max_c = max(abs(point.x), abs(point.y), abs(point.z))
        if max_c == abs(point.x):
            return Vector(point.x, 0, 0)
        elif max_c == abs(point.y):
            return Vector(0, point.y, 0)
        else:
            return Vector(0, 0, point.z)

    def _local_intersect(self, ray: Ray):
        xt_min, xt_max = _check_axis(ray.origin.x, ray.direction.x)
        yt_min, yt_max = _check_axis(ray.origin.y, ray.direction.y)
        zt_min, zt_max = _check_axis(ray.origin.z, ray.direction.z)

        t_min = max(xt_min, yt_min, zt_min)
        t_max = min(xt_max, yt_max, zt_max)

        if t_min > t_max:
            return Intersections()

        return Intersections(Intersection(t_min, self), Intersection(t_max, self))

