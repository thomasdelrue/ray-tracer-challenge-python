from abc import ABC, abstractmethod
from .matrices import Matrix
from .shapes import Shape
from .tuples import Color, Point
import math


class Pattern(ABC):
    def __init__(self):
        self.transformation: Matrix = Matrix.identity()

    def pattern_at_shape(self, shape: Shape, world_point: Point) -> Color:
        object_point = shape.transformation.inverse() * world_point
        pattern_point = self.transformation.inverse() * object_point
        return self.pattern_at(pattern_point)

    @abstractmethod
    def pattern_at(self, point: Point) -> Color:
        ...


class StripePattern(Pattern):
    def __init__(self, first_color: Color, second_color: Color):
        super().__init__()
        self.first_color = first_color
        self.second_color = second_color

    def pattern_at(self, point: Point) -> Color:
        if math.floor(point.x) % 2 == 0:
            return self.first_color
        else:
            return self.second_color
