from dataclasses import dataclass
from .tuples import Color, Point
import math


@dataclass
class Pattern:
    a: Color
    b: Color


def stripe_pattern(first_color: Color, second_color: Color):
    return Pattern(first_color, second_color)


def stripe_at(pattern: Pattern, point: Point) -> Color:
    if math.floor(point.x) % 2 == 0:
        return pattern.a
    else:
        return pattern.b
