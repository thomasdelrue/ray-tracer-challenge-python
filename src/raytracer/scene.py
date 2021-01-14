from .intersections import Intersections, Computations
from .rays import Ray
from .tuples import Color, Point, dot
from math import sqrt


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

    def shade_hit(self, comps: Computations, remaining: int = 4):
        shadowed = self.is_shadowed(comps.over_point)
        surface = comps.object.material.lighting(comps.object, self.light_source, comps.point, comps.eyev,
                                                 comps.normalv, shadowed)
        reflected = self.reflected_color(comps, remaining)
        refracted = self.refracted_color(comps, remaining)
        return surface + reflected + refracted

    def color_at(self, ray: Ray, remaining: int = 4) -> Color:
        xs = self.intersect(ray)
        hit = xs.hit()
        if not hit:
            return Color.black()
        comps = hit.prepare_computations(ray, xs)
        return self.shade_hit(comps, remaining)

    def is_shadowed(self, point: Point) -> bool:
        v = self.light_source.position - point
        distance = v.magnitude
        direction = v.normalize()

        r = Ray(point, direction)
        xs = self.intersect(r)
        hit = xs.hit()

        return hit is not None and hit.t < distance

    def reflected_color(self, comps: Computations, remaining: int = 4) -> Color:
        if remaining <= 0:
            return Color.black()

        if comps.object.material.reflective == 0.0:
            return Color.black()

        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, remaining - 1)

        return color * comps.object.material.reflective

    def refracted_color(self, comps: Computations, remaining: int = 4) -> Color:
        if remaining <= 0:
            return Color.black()

        if comps.object.material.transparency == 0.0:
            return Color.black()

        # find ratio of first index of refraction to second. (inverted from definition of Snell's Law)
        n_ratio = comps.n1 / comps.n2
        # cos(theta_i) is the same as the dot product of the two vectors
        cos_i = dot(comps.eyev, comps.normalv)
        # find sin(theta_t)^2 via trigonometric identity
        sin2_t = n_ratio ** 2 * (1 - cos_i ** 2)
        if sin2_t > 1.0:
            return Color.black()

        cos_t = sqrt(1.0 - sin2_t)
        direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
        refracted_ray = Ray(comps.under_point, direction)

        return self.color_at(refracted_ray, remaining - 1) * comps.object.material.transparency
