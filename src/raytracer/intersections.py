from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import Optional
from . import EPSILON
from .rays import Ray
from .tuples import Point, Vector, dot


@dataclass
class Computations:
    t: float
    object: object
    point: Point
    eyev: Vector
    normalv: Vector
    reflectv: Vector = 0.0
    n1: float = 0.0
    n2: float = 0.0

    def __post_init__(self):
        if dot(self.normalv, self.eyev) < 0:
            self.normalv = -self.normalv
            self.inside = True
        else:
            self.inside = False
        self.over_point = self.point + self.normalv * EPSILON
        self.under_point = self.point - self.normalv * EPSILON

    def schlick(self) -> float:
        cos = dot(self.eyev, self.normalv)

        # total internal reflection can only occur if n1 > n2
        if self.n1 > self.n2:
            n_ratio = self.n1 / self.n2
            sin2_t = n_ratio ** 2 * (1.0 - cos ** 2)
            if sin2_t > 1.0:
                return 1.0
            # compute cosine theta_t using trig identity
            cos_t = sqrt(1.0 - sin2_t)
            cos = cos_t

        r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2

        return r0 + (1 - r0) * (1 - cos) ** 5


class Intersections:
    def __init__(self, *intersections):
        self._collection = sorted(intersections, key=lambda intersection: intersection.t)
        self._sorted = True

    @property
    def count(self):
        return len(self._collection)

    def append(self, intersection: Intersection, to_sort: bool = True):
        self._collection.append(intersection)
        self._sorted = False
        if to_sort:
            self.sort()

    def extend(self, intersections: Intersections, to_sort: bool = True):
        for intersection in intersections:
            self._collection.append(intersection)
        self._sorted = False
        if to_sort:
            self.sort()

    def sort(self):
        if not self._sorted:
            self._collection = sorted(self._collection, key=lambda x: x.t)
            self._sorted = True

    def __getitem__(self, item) -> Intersection:
        return self._collection[item]

    def hit(self) -> Optional[Intersection]:
        for intersection in self._collection:
            # return the first non-negative t intersection from the ordered list
            if intersection.t >= 0:
                return intersection

    def __repr__(self):
        return self._collection.__repr__()


class Intersection:
    def __init__(self, t: float, _object: object):
        self.t = t
        self.object = _object

    def prepare_computations(self, ray: Ray, xs: Intersections = Intersections()) -> Computations:
        point = ray.position(self.t)
        eyev = -ray.direction
        normalv = self.object.normal_at(point)
        reflectv = ray.direction.reflect(normalv)

        containers = []
        n1, n2 = 0.0, 0.0
        for i in xs:
            if i == self:
                if len(containers) == 0:
                    n1 = 1.0
                else:
                    n1 = containers[-1].material.refractive_index
            if i.object in containers:
                containers.remove(i.object)
            else:
                containers.append(i.object)
            if i == self:
                if len(containers) == 0:
                    n2 = 1.0
                else:
                    n2 = containers[-1].material.refractive_index
                break

        return Computations(self.t, self.object, point, eyev, normalv, reflectv, n1, n2)

    def __repr__(self):
        return f'Intersection(t={self.t}, object={self.object})'
