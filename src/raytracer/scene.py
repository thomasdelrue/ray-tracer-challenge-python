from .intersections import Intersections, Computations
from .rays import Ray
from .tuples import Color, Point


class World:
    def __init__(self):
        self.objects = []
        self.light_source = None

    def add(self, *objects):
        self.objects.extend(objects)

    def intersect(self, ray: Ray) -> Intersections:
        results = []
        for obj in self.objects:
            results += obj.intersect(ray)
        return Intersections(*results)

    def shade_hit(self, comps: Computations):
        shadowed = self.is_shadowed(comps.over_point)
        return comps.object.material.lighting(self.light_source, comps.point, comps.eyev, comps.normalv, shadowed)

    def color_at(self, ray: Ray) -> Color:
        xs = self.intersect(ray)
        hit = xs.hit()
        if not hit:
            return Color.black()
        comps = hit.prepare_computations(ray)
        return self.shade_hit(comps)

    def is_shadowed(self, point: Point) -> bool:
        v = self.light_source.position - point
        distance = v.magnitude
        direction = v.normalize()

        r = Ray(point, direction)
        xs = self.intersect(r)
        hit = xs.hit()

        return hit is not None and hit.t < distance
