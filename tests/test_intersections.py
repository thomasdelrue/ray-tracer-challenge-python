from raytracer.intersections import Intersection, Intersections
from raytracer.spheres import Sphere


class TestIntersections:
    def test_intersection_encapsulates_t_and_object(self):
        s = Sphere()
        i = Intersection(3.5, s)
        assert i.t == 3.5
        assert i.object == s

    def test_aggregate_intersections(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i1, i2)
        assert xs.count == 2
        assert xs[0].t == 1
        assert xs[1].t == 2

    def test_hit_when_all_intersections_have_positive_t(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i2, i1)
        assert xs.hit() == i1

    def test_hit_when_some_intersections_have_negative_t(self):
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(1, s)
        xs = Intersections(i2, i1)
        assert xs.hit() == i2

    def test_hit_when_all_intersections_have_negative_t(self):
        s = Sphere()
        i1 = Intersection(-2, s)
        i2 = Intersection(-1, s)
        xs = Intersections(i2, i1)
        assert xs.hit() is None

    def test_hit_is_always_lowest_nonnegative_intersection(self):
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(7, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(2, s)
        xs = Intersections(i1, i2, i3, i4)
        assert xs.hit() == i4
