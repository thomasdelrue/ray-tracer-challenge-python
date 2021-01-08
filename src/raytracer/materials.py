from . import EPSILON
from .lights import PointLight
from .tuples import Color, Vector, Point, dot
import math


class Material:
    def __init__(self):
        self.color = Color(1, 1, 1)
        self.ambient = 0.1
        self.diffuse = 0.9
        self.specular = 0.9
        self.shininess = 200.0
        self.pattern = None

    def __eq__(self, other):
        return self.color == other.color and \
            abs(self.ambient - other.ambient) < EPSILON and \
            abs(self.diffuse - other.diffuse) < EPSILON and \
            abs(self.specular - other.specular) < EPSILON and \
            abs(self.shininess - other.shininess) < EPSILON and \
            self.pattern == other.pattern

    def lighting(self, _object, light: PointLight, point: Point, eyev: Vector, normalv: Vector,
                 in_shadow: bool = False) -> Color:
        if self.pattern:
            color = self.pattern.pattern_at_shape(_object, point)
        else:
            color = self.color

        # combine surface color with light's color/intensity
        effective_color = color * light.intensity

        # find direction to light source
        lightv = (light.position - point).normalize()

        # compute ambient contribution
        ambient = effective_color * self.ambient
        diffuse = Color.black()
        specular = Color.black()

        if not in_shadow:
            # light_dot_normal represents the cosine of the angle between light vector and
            # normal vector. Negative number means light is on other side of surface
            light_dot_normal = dot(lightv, normalv)
            if light_dot_normal < 0:
                diffuse = Color.black()
                specular = Color.black()
            else:
                diffuse = effective_color * self.diffuse * light_dot_normal

                # reflect_dot_eye represents the cosine of the angle between the reflection
                # vector and eye vector. Negative number means light reflects away from the eye
                reflectv = (-lightv).reflect(normalv)
                reflect_dot_eye = dot(reflectv, eyev)
                if reflect_dot_eye <= 0:
                    specular = Color.black()
                else:
                    factor = math.pow(reflect_dot_eye, self.shininess)
                    specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular
