from .tuples import Color, Point


class PointLight:
    def __init__(self, position: Point, intensity: Color):
        self.position = position
        self.intensity = intensity
