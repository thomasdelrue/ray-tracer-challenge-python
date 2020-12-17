from raytracer.lights import PointLight
from raytracer.tuples import Color, Point


class TestLights:
    def test_point_light_has_position_and_intensity(self):
        intensity = Color(1, 1, 1)
        position = Point(0, 0, 0)
        light = PointLight(position, intensity)
        assert light.position == position
        assert light.intensity == intensity

