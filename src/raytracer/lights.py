from .tuples import Color, Point


class PointLight:
    def __init__(self, position: Point, intensity: Color):
        self.position = position
        self.intensity = intensity

    def __repr__(self):
        return f'PointLight(position={self.position}, intensity={self.intensity})'
