from math import pi, sqrt
from raytracer.camera import Camera
from raytracer.matrices import Matrix, rotation_y, translation
from raytracer.tuples import Point, Vector
import pytest


class TestCamera:
    def test_construct_camera(self):
        hsize = 160
        vsize = 120
        field_of_view = pi / 2
        c = Camera(hsize, vsize, field_of_view)
        assert c.hsize == 160
        assert c.vsize == 120
        assert c.field_of_view == pi / 2
        assert c.transformation == Matrix.identity()

    def test_pixel_size_for_horizontal_canvas(self):
        c = Camera(200, 125, pi / 2)
        assert c.pixel_size == pytest.approx(0.01)

    def test_pixel_size_for_vertical_canvas(self):
        c = Camera(125, 200, pi / 2)
        assert c.pixel_size == pytest.approx(0.01)

    def test_construct_ray_through_center_of_canvas(self):
        c = Camera(201, 101, pi / 2)
        r = c.ray_for_pixel(100, 50)
        assert r.origin == Point(0, 0, 0)
        assert r.direction == Vector(0, 0, -1)

    def test_construct_ray_through_corner_of_canvas(self):
        c = Camera(201, 101, pi / 2)
        r = c.ray_for_pixel(0, 0)
        assert r.origin == Point(0, 0, 0)
        assert r.direction == Vector(0.66519, 0.33259, -0.66851)

    def test_construct_ray_when_camera_is_transformed(self):
        c = Camera(201, 101, pi / 2)
        c.transformation = rotation_y(pi / 4) * translation(0, -2, 5)
        r = c.ray_for_pixel(100, 50)
        assert r.origin == Point(0, 2, -5)
        assert r.direction == Vector(sqrt(2) / 2, 0, -sqrt(2) / 2)

