from .intersections import Intersections
from .rays import Ray


class World:
    def __init__(self):
        self.objects = []
        self.light = None

    def add(self, *objects):
        self.objects.extend(objects)

    def intersect(self, ray: Ray) -> Intersections:
        results = []
        for obj in self.objects:
            results += obj.intersect(ray)
        return Intersections(*results)
