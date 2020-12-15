from __future__ import annotations
from enum import Enum
from math import sqrt
from typing import NamedTuple

EPSILON = 0.00001


class TupleType(Enum):
    POINT = 1.0
    VECTOR = 0.0


class Tuple(NamedTuple):
    x: float
    y: float
    z: float
    w: float

    @property
    def type(self) -> str:
        return TupleType(self.w).name

    def __add__(self, other):
        return Tuple(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Tuple(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError(f'multiplying a tuple by {type(other)} not supported')
        return self._scalar(other)

    def __rmul__(self, other):
        return self * other

    def _scalar(self, scalar: float):
        return Tuple(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError(f'Dividing a tuple by {type(other)} not supported')
        if other == 0:
            raise ZeroDivisionError
        scalar = 1.0 / other
        return self._scalar(scalar)

    def __eq__(self, other):
        return abs(self.x - other.x) < EPSILON and abs(self.y - other.y) < EPSILON and \
               abs(self.z - other.z) < EPSILON and abs(self.w - other.w) < EPSILON


class Point(Tuple):
    def __new__(cls, *args, **kwargs):
        kwargs['w'] = TupleType.POINT.value
        return super().__new__(cls, *args, **kwargs)


class Vector(Tuple):
    def __new__(cls, *args, **kwargs):
        kwargs['w'] = TupleType.VECTOR.value
        return super().__new__(cls, *args, **kwargs)

    @property
    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        magnitude = self.magnitude
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)


def dot(t1: Tuple, t2: Tuple) -> float:
    return t1.x * t2.x + t1.y * t2.y + t1.z * t2.z + t1.w * t2.w


def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(v1.y * v2.z - v1.z * v2.y,
                  v1.z * v2.x - v1.x * v2.z,
                  v1.x * v2.y - v1.y * v2.x)


class Color(NamedTuple):
    red: float
    green: float
    blue: float

    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __sub__(self, other):
        return Color(self.red - other.red, self.green - other.green, self.blue - other.blue)

    def __eq__(self, other):
        return abs(self.red - other.red) < EPSILON and abs(self.green - other.green) < EPSILON and \
               abs(self.blue - other.blue) < EPSILON

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Color(self.red * other, self.green * other, self.blue * other)
        if isinstance(other, Color):
            return hadamard_product(self, other)
        raise NotImplementedError

    def __rmul__(self, other):
        return self * other


def hadamard_product(c1: Color, c2: Color):
    return Color(c1.red * c2.red, c1.green * c2.green, c1.blue * c2.blue)
