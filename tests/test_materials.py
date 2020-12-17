from math import sqrt
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.tuples import Color, Point, Vector
import pytest


class TestMaterials:
    @pytest.fixture
    def fixture(self):
        return {'m': Material(), 'position': Point(0, 0, 0)}

    def test_default_material(self):
        m = Material()
        assert m.color == Color(1, 1, 1)
        assert m.ambient == 0.1
        assert m.diffuse == 0.9
        assert m.specular == 0.9
        assert m.shininess == 200.0

    def test_lighting_with_eye_between_light_and_surface(self, fixture):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = fixture['m'].lighting(light, fixture['position'], eyev, normalv)
        assert result == Color(1.9, 1.9, 1.9)

    def test_lighting_with_eye_between_light_and_surface_eye_offset_45(self, fixture):
        eyev = Vector(0, sqrt(2) / 2, -sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = fixture['m'].lighting(light, fixture['position'], eyev, normalv)
        assert result == Color(1.0, 1.0, 1.0)

    def test_lighting_eye_opposite_surface_light_offset_45(self, fixture):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = fixture['m'].lighting(light, fixture['position'], eyev, normalv)
        assert result == Color(0.7364, 0.7364, 0.7364)

    def test_lighting_eye_in_path_of_reflection_vector(self, fixture):
        eyev = Vector(0, -sqrt(2) / 2, -sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = fixture['m'].lighting(light, fixture['position'], eyev, normalv)
        assert result == Color(1.6364, 1.6364, 1.6364)

    def test_lighting_light_behind_surface(self, fixture):
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
        result = fixture['m'].lighting(light, fixture['position'], eyev, normalv)
        assert result == Color(0.1, 0.1, 0.1)



