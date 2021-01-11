from __future__ import annotations
from abc import ABC, abstractmethod
from .matrices import Matrix
from .shapes import Shape
from .tuples import Color, Point
import math


class Pattern(ABC):
    def __init__(self, first_color: Color, second_color: Color):
        self.first_color = first_color
        self.second_color = second_color
        self.transformation: Matrix = Matrix.identity()

    def pattern_at_shape(self, shape: Shape, world_point: Point) -> Color:
        object_point = shape.transformation.inverse() * world_point
        pattern_point = self.transformation.inverse() * object_point
        return self.pattern_at(pattern_point)

    @abstractmethod
    def pattern_at(self, point: Point) -> Color:
        ...


class StripePattern(Pattern):
    def pattern_at(self, point: Point) -> Color:
        if math.floor(point.x) % 2 == 0:
            return self.first_color
        else:
            return self.second_color


class GradientPattern(Pattern):
    def pattern_at(self, point: Point) -> Color:
        distance = self.second_color - self.first_color
        fraction = point.x - math.floor(point.x)
        return self.first_color + distance * fraction


class RingPattern(Pattern):
    def pattern_at(self, point: Point) -> Color:
        if math.floor(math.sqrt(point.x * point.x + point.z * point.z)) % 2 == 0:
            return self.first_color
        else:
            return self.second_color


class CheckersPattern(Pattern):
    def pattern_at(self, point: Point) -> Color:
        if (math.floor(point.x) + math.floor(point.y) + math.floor(point.z)) % 2 == 0:
            return self.first_color
        else:
            return self.second_color


class RadialGradientPattern(Pattern):
    def pattern_at(self, point: Point) -> Color:
        distance = self.second_color - self.first_color
        position = math.sqrt(point.x * point.x + point.z * point.z)
        fraction = position - math.floor(position)
        return self.first_color + distance * fraction
