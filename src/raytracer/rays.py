from .tuples import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def position(self, t: float):
        return self.origin + self.direction * t

