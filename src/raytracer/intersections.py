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

    def __post_init__(self):
        if dot(self.normalv, self.eyev) < 0:
            self.normalv = -self.normalv
            self.inside = True
        else:
            self.inside = False
        self.over_point = self.point + self.normalv * EPSILON


class Intersection:
    def __init__(self, t: float, _object: object):
        self.t = t
        self.object = _object

    def prepare_computations(self, ray: Ray) -> Computations:
        point = ray.position(self.t)
        eyev = -ray.direction
        normalv = self.object.normal_at(point)
        return Computations(self.t, self.object, point, eyev, normalv)

    def __repr__(self):
        return f'Intersection(t={self.t}, object={self.object})'


class Intersections:
    def __init__(self, *intersections):
        self._container = sorted(intersections, key=lambda intersection: intersection.t)

    @property
    def count(self):
        return len(self._container)

    def __getitem__(self, item):
        return self._container[item]

    def hit(self) -> Optional[Intersection]:
        for intersection in self._container:
            # return the first non-negative t intersection from the ordered list
            if intersection.t >= 0:
                return intersection


