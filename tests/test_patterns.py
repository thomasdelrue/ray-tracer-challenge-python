from raytracer.matrices import scaling, translation
from raytracer.patterns import stripe_pattern, stripe_at, stripe_at_object
from raytracer.shapes import Sphere
from raytracer.tuples import Color, Point


class TestPatterns:
    def test_create_stripe_pattern(self):
        pattern = stripe_pattern(Color.white(), Color.black())
        assert pattern.a == Color.white()
        assert pattern.b == Color.black()

    def test_stripe_pattern_constant_in_y(self):
        pattern = stripe_pattern(Color.white(), Color.black())
        assert stripe_at(pattern, Point(0, 0, 0)) == Color.white()
        assert stripe_at(pattern, Point(0, 1, 0)) == Color.white()
        assert stripe_at(pattern, Point(0, 2, 0)) == Color.white()

    def test_stripe_pattern_constant_in_z(self):
        pattern = stripe_pattern(Color.white(), Color.black())
        assert stripe_at(pattern, Point(0, 0, 0)) == Color.white()
        assert stripe_at(pattern, Point(0, 0, 1)) == Color.white()
        assert stripe_at(pattern, Point(0, 0, 2)) == Color.white()

    def test_stripe_pattern_alternates_in_x(self):
        pattern = stripe_pattern(Color.white(), Color.black())
        assert stripe_at(pattern, Point(0, 0, 0)) == Color.white()
        assert stripe_at(pattern, Point(0.9, 0, 0)) == Color.white()
        assert stripe_at(pattern, Point(1, 0, 0)) == Color.black()
        assert stripe_at(pattern, Point(-0.1, 0, 0)) == Color.black()
        assert stripe_at(pattern, Point(-1, 0, 0)) == Color.black()
        assert stripe_at(pattern, Point(-1.1, 0, 0)) == Color.white()

    def test_stripes_with_object_transformation(self):
        obj = Sphere()
        obj.transformation = scaling(2, 2, 2)
        pattern = stripe_pattern(Color.white(), Color.black())
        c = stripe_at_object(pattern, obj, Point(1.5, 0, 0))
        assert c == Color.white()

    def test_stripes_with_pattern_transformation(self):
        obj = Sphere()
        pattern = stripe_pattern(Color.white(), Color.black())
        pattern.transformation = scaling(2, 2, 2)
        c = stripe_at_object(pattern, obj, Point(1.5, 0, 0))
        assert c == Color.white()

    def test_stripes_with_both_object_and_pattern_transformation(self):
        obj = Sphere()
        obj.transformation = scaling(2, 2, 2)
        pattern = stripe_pattern(Color.white(), Color.black())
        pattern.transformation = translation(0.5, 0, 0)
        c = stripe_at_object(pattern, obj, Point(2.5, 0, 0))
        assert c == Color.white()

