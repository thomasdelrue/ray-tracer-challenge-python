from __future__ import annotations
from dataclasses import dataclass
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


class Intersections:
    def __init__(self, *intersections):
        self._collection = sorted(intersections, key=lambda intersection: intersection.t)

    @property
    def count(self):
        return len(self._collection)

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
