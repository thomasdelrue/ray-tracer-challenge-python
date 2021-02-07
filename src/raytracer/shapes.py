from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from . import EPSILON, INF
from .intersections import Intersection, Intersections
from .materials import Material
from .matrices import Matrix
from .rays import Ray
from .tuples import Point, Vector, dot, cross
import itertools
import math


class Shape(ABC):
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self.transformation = Matrix.identity()
        self.material = Material()
        self.parent: Optional[Shape] = None

    def intersect(self, ray: Ray) -> Intersections:
        local_ray = ray.transform(self.transformation.inverse())
        return self._local_intersect(local_ray)

    @abstractmethod
    def _local_intersect(self, ray: Ray) -> Intersections:
        ...

    def normal_at(self, world_point: Point) -> Vector:
        local_point = self.world_to_object(world_point)
        local_normal = self._local_normal_at(local_point)
        return self.normal_to_world(local_normal)

    @abstractmethod
    def _local_normal_at(self, point: Point) -> Vector:
        ...

    def world_to_object(self, point: Point) -> Point:
        if self.parent:
            point = self.parent.world_to_object(point)
        return self.transformation.inverse() * point

    def normal_to_world(self, normal: Vector) -> Vector:
        x, y, z, _ = self.transformation.inverse().transpose() * normal
        normal = Vector(x, y, z).normalize()

        if self.parent:
            normal = self.parent.normal_to_world(normal)

        return normal

    @abstractmethod
    def bounds(self) -> BoundingBox:
        ...

    def parent_space_bounds(self) -> BoundingBox:
        return self.bounds().transform(self.transformation)


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

    def bounds(self) -> BoundingBox:
        return BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))

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

    def bounds(self) -> BoundingBox:
        return BoundingBox(Point(-INF, 0, -INF), Point(INF, 0, INF))


def _check_axis(origin: float, direction: float, _min: float = 1, _max: float = 1) -> (float, float):
    t_min_numerator = _min - origin
    t_max_numerator = _max - origin

    if abs(direction) >= EPSILON:
        t_min = t_min_numerator / direction
        t_max = t_max_numerator / direction
    else:
        t_min = t_min_numerator * INF
        t_max = t_max_numerator * INF

    if t_min > t_max:
        t_min, t_max = t_max, t_min

    return t_min, t_max


class Cube(Shape):
    def __init__(self):
        super().__init__()
        self.minimum = Point(-1, -1, -1)
        self.maximum = Point(1, 1, 1)

    def _local_normal_at(self, point: Point) -> Vector:
        max_c = max(abs(point.x), abs(point.y), abs(point.z))
        if max_c == abs(point.x):
            return Vector(point.x, 0, 0)
        elif max_c == abs(point.y):
            return Vector(0, point.y, 0)
        else:
            return Vector(0, 0, point.z)

    def _local_intersect(self, ray: Ray):
        xt_min, xt_max = _check_axis(ray.origin.x, ray.direction.x, self.minimum.x, self.maximum.x)
        yt_min, yt_max = _check_axis(ray.origin.y, ray.direction.y, self.minimum.y, self.maximum.y)
        zt_min, zt_max = _check_axis(ray.origin.z, ray.direction.z, self.minimum.z, self.maximum.z)

        t_min = max(xt_min, yt_min, zt_min)
        t_max = min(xt_max, yt_max, zt_max)

        if t_min > t_max:
            return Intersections()

        return Intersections(Intersection(t_min, self), Intersection(t_max, self))

    def bounds(self) -> BoundingBox:
        return BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))


# Checks to see if the intersection at 't' is within a radius
# from the y axis
def _check_cap(ray: Ray, t: float, radius: float = 1.0) -> bool:
    x = ray.origin.x + t * ray.direction.x
    z = ray.origin.z + t * ray.direction.z
    return x * x + z * z <= radius


def _calculate_intersections(a: float, b: float, c: float, ray: Ray, _object) -> Intersections:
    xs = Intersections()
    discriminant = b ** 2 - 4 * a * c

    # ray does not intersect object
    if discriminant < 0:
        return Intersections()

    t0 = (-b - math.sqrt(discriminant)) / (2 * a)
    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    if t0 > t1:
        t0, t1 = t1, t0

    y0 = ray.origin.y + t0 * ray.direction.y
    if _object.minimum < y0 < _object.maximum:
        xs.append(Intersection(t0, _object))

    y1 = ray.origin.y + t1 * ray.direction.y
    if _object.minimum < y1 < _object.maximum:
        xs.append(Intersection(t1, _object))
    return xs


class Cylinder(Shape):
    def __init__(self, closed: bool = False):
        super().__init__()
        self.minimum = -INF
        self.maximum = INF
        self.closed = closed

    def _local_normal_at(self, point: Point) -> Vector:
        dist = point.x ** 2 + point.z ** 2

        if dist < 1 and point.y >= self.maximum - EPSILON:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + EPSILON:
            return Vector(0, -1, 0)
        else:
            return Vector(point.x, 0, point.z)

    def _local_intersect(self, ray: Ray) -> Intersections:
        xs = Intersections()

        a = ray.direction.x ** 2 + ray.direction.z ** 2

        # ray is not parallel to y axis
        if abs(a) >= EPSILON:
            b = 2 * ray.origin.x * ray.direction.x + 2 * ray.origin.z * ray.direction.z
            c = ray.origin.x ** 2 + ray.origin.z ** 2 - 1

            xs.extend(_calculate_intersections(a, b, c, ray, self))

        xs.extend(self.intersect_caps(ray))

        return xs

    def intersect_caps(self, ray: Ray) -> Intersections:
        xs = Intersections()
        if not self.closed or abs(ray.direction.y) < EPSILON:
            return xs

        t = (self.minimum - ray.origin.y) / ray.direction.y
        if _check_cap(ray, t):
            xs.append(Intersection(t, self))

        t = (self.maximum - ray.origin.y) / ray.direction.y
        if _check_cap(ray, t):
            xs.append(Intersection(t, self))

        return xs

    def bounds(self) -> BoundingBox:
        return BoundingBox(Point(-1, self.minimum, -1), Point(1, self.maximum, 1))


class Cone(Shape):
    def __init__(self, closed: bool = False):
        super().__init__()
        self.minimum = -INF
        self.maximum = INF
        self.closed = closed

    def _local_intersect(self, ray: Ray) -> Intersections:
        xs = Intersections()

        a = ray.direction.x ** 2 - ray.direction.y ** 2 + ray.direction.z ** 2
        b = 2 * ray.origin.x * ray.direction.x - 2 * ray.origin.y * ray.direction.y + 2 * ray.origin.z * ray.direction.z
        c = ray.origin.x ** 2 + ray.origin.z ** 2 - ray.origin.y ** 2

        # ray is not parallel to y axis
        if abs(a) >= EPSILON:
            xs.extend(_calculate_intersections(a, b, c, ray, self))
        elif abs(b) >= EPSILON:
            t = -c / (2 * b)
            xs.append(Intersection(t, self))

        xs.extend(self.intersect_caps(ray))

        return xs

    def intersect_caps(self, ray: Ray) -> Intersections:
        xs = Intersections()
        if not self.closed or abs(ray.direction.y) < EPSILON:
            return xs

        t = (self.minimum - ray.origin.y) / ray.direction.y
        if _check_cap(ray, t, abs(self.minimum)):
            xs.append(Intersection(t, self))

        t = (self.maximum - ray.origin.y) / ray.direction.y
        if _check_cap(ray, t, abs(self.maximum)):
            xs.append(Intersection(t, self))

        return xs

    def _local_normal_at(self, point: Point) -> Vector:
        dist = point.x ** 2 + point.z ** 2

        if dist < 1 and point.y >= self.maximum - EPSILON:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + EPSILON:
            return Vector(0, -1, 0)
        else:
            y = math.sqrt(dist)
            if point.y > 0:
                y = -y
            return Vector(point.x, y, point.z)

    def bounds(self) -> BoundingBox:
        limit = max(abs(self.minimum), abs(self.maximum))
        return BoundingBox(Point(-limit, self.minimum, -limit), Point(limit, self.maximum, limit))


class Group(Shape):
    def __init__(self):
        super().__init__()
        self._collection: List[Shape] = []

    @property
    def empty(self):
        return len(self._collection) == 0

    def add_children(self, *children: Shape):
        for child in children:
            child.parent = self
            self._collection.append(child)

    def __getitem__(self, index) -> Shape:
        return self._collection[index]

    def _local_normal_at(self, point: Point) -> Vector:
        raise NotImplementedError

    def _local_intersect(self, ray: Ray) -> Intersections:
        xs = Intersections()
        if self.bounds().intersect(ray).count == 0:
            return xs

        for _object in self:
            xs.extend(_object.intersect(ray), to_sort=False)
        xs.sort()
        return xs

    def bounds(self) -> BoundingBox:
        box = BoundingBox()
        for child in self:
            box.merge(child.parent_space_bounds())
        return box


class BoundingBox(Cube):
    def __init__(self, minimum: Point = Point(INF, INF, INF),
                 maximum: Point = Point(-INF, -INF, -INF)):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum

    def include(self, p: Point) -> None:
        x, y, z = min(self.minimum.x, p.x), min(self.minimum.y, p.y), min(self.minimum.z, p.z)
        self.minimum = Point(x, y, z)
        x, y, z = max(self.maximum.x, p.x), max(self.maximum.y, p.y), max(self.maximum.z, p.z)
        self.maximum = Point(x, y, z)

    def merge(self, box: BoundingBox) -> None:
        self.include(box.minimum)
        self.include(box.maximum)

    def contains_point(self, point: Point) -> bool:
        return self.minimum.x <= point.x <= self.maximum.x and \
               self.minimum.y <= point.y <= self.maximum.y and \
               self.minimum.z <= point.z <= self.maximum.z

    def contains_box(self, box: BoundingBox) -> bool:
        return self.contains_point(box.minimum) and self.contains_point(box.maximum)

    def transform(self, matrix: Matrix):
        edges = [Point(x, y, z) for x, y, z in itertools.product((self.minimum.x, self.maximum.x),
                                                                 (self.minimum.y, self.maximum.y),
                                                                 (self.minimum.z, self.maximum.z))]
        new_box = BoundingBox()
        for edge in edges:
            new_box.include(matrix * edge)
        return new_box


class Triangle(Shape):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.e1 = p2 - p1
        self.e2 = p3 - p1
        self.normal = cross(self.e2, self.e1).normalize()

    def _local_intersect(self, ray: Ray) -> Intersections:
        dir_cross_e2 = cross(ray.direction, self.e2)
        determinant = dot(self.e1, dir_cross_e2)
        if abs(determinant) < EPSILON:
            return Intersections()

        f = 1.0 / determinant
        p1_to_origin = ray.origin - self.p1
        u = f * dot(p1_to_origin, dir_cross_e2)
        if u < 0 or u > 1:
            return Intersections()

        origin_cross_e1 = cross(p1_to_origin, self.e1)
        v = f * dot(ray.direction, origin_cross_e1)
        if v < 0 or (u + v) > 1:
            return Intersections()

        t = f * dot(self.e2, origin_cross_e1)
        return Intersections(Intersection(t, self))

    def _local_normal_at(self, point: Point) -> Vector:
        return self.normal

    def bounds(self) -> BoundingBox:
        box = BoundingBox()
        box.include(self.p1)
        box.include(self.p2)
        box.include(self.p3)
        return box

