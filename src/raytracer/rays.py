from .matrices import Matrix
from .tuples import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def position(self, t: float):
        return self.origin + self.direction * t

    def transform(self, transformation: Matrix):
        return Ray(transformation * self.origin, transformation * self.direction)


