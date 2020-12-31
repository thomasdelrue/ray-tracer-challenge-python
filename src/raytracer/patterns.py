from dataclasses import dataclass
from .matrices import Matrix
from .tuples import Color, Point
import math


@dataclass
class Pattern:
    a: Color
    b: Color
    transformation: Matrix = Matrix.identity()


def stripe_pattern(first_color: Color, second_color: Color):
    return Pattern(first_color, second_color)


def stripe_at(pattern: Pattern, point: Point) -> Color:
    if math.floor(point.x) % 2 == 0:
        return pattern.a
    else:
        return pattern.b


def stripe_at_object(pattern: Pattern, _object, world_point: Point) -> Color:
    object_point = _object.transformation.inverse() * world_point
    pattern_point = pattern.transformation.inverse() * object_point
    return stripe_at(pattern, pattern_point)
