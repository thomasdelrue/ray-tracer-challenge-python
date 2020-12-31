from math import sqrt
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.patterns import stripe_pattern
from raytracer.shapes import Sphere
from raytracer.tuples import Color, Point, Vector
import pytest


class TestMaterials:
    @pytest.fixture
    def background(self):
        return {'m': Material(), 'position': Point(0, 0, 0)}

    def test_default_material(self):
        m = Material()
        assert m.color == Color(1, 1, 1)
        assert m.ambient == 0.1
        assert m.diffuse == 0.9
        assert m.specular == 0.9
        assert m.shininess == 200.0

    def test_lighting_with_eye_between_light_and_surface(self, background):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv)
        assert result == Color(1.9, 1.9, 1.9)

    def test_lighting_with_eye_between_light_and_surface_eye_offset_45(self, background):
        eyev = Vector(0, sqrt(2) / 2, -sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv)
        assert result == Color(1.0, 1.0, 1.0)

    def test_lighting_eye_opposite_surface_light_offset_45(self, background):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv)
        assert result == Color(0.7364, 0.7364, 0.7364)

    def test_lighting_eye_in_path_of_reflection_vector(self, background):
        eyev = Vector(0, -sqrt(2) / 2, -sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv)
        assert result == Color(1.6364, 1.6364, 1.6364)

    def test_lighting_light_behind_surface(self, background):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv)
        assert result == Color(0.1, 0.1, 0.1)

    def test_lighting_with_surface_in_shadow(self, background):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        in_shadow = True
        result = background['m'].lighting(Sphere(), light, background['position'], eyev, normalv, in_shadow)
        assert result == Color(0.1, 0.1, 0.1)

    def test_lighting_with_pattern_applied(self):
        m = Material()
        m.pattern = stripe_pattern(Color.white(), Color.black())
        m.ambient = 1
        m.diffuse = 0
        m.specular = 0
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color.white())
        c1 = m.lighting(Sphere(), light, Point(0.9, 0, 0), eyev, normalv, False)
        c2 = m.lighting(Sphere(), light, Point(1.1, 0, 0), eyev, normalv, False)
        assert c1 == Color.white()
        assert c2 == Color.black()



