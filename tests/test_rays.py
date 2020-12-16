from raytracer.matrices import translation, scaling
from raytracer.rays import Ray
from raytracer.tuples import Point, Vector


class TestRays:
    def test_create_ray(self):
        origin = Point(1, 2, 3)
        direction = Vector(4, 5, 6)
        r = Ray(origin, direction)
        assert r.origin == origin
        assert r.direction == direction

    def test_compute_point_from_distance(self):
        r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
        assert r.position(0) == Point(2, 3, 4)
        assert r.position(1) == Point(3, 3, 4)
        assert r.position(-1) == Point(1, 3, 4)
        assert r.position(2.5) == Point(4.5, 3, 4)

    def test_translate_ray(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = translation(3, 4, 5)
        r2 = r.transform(m)
        assert r2.origin == Point(4, 6, 8)
        assert r2.direction == Vector(0, 1, 0)

    def test_scale_ray(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = scaling(2, 3, 4)
        r2 = r.transform(m)
        assert r2.origin == Point(2, 6, 12)
        assert r2.direction == Vector(0, 3, 0)

