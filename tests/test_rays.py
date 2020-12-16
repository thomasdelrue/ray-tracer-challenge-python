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
