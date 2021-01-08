from raytracer.matrices import Matrix, scaling, translation
from raytracer.patterns import Pattern, StripePattern
from raytracer.shapes import Shape, Sphere
from raytracer.tuples import Color, Point


def test_pattern():
    class TestPattern(Pattern):
        def pattern_at(self, point: Point) -> Color:
            return Color(point.x, point.y, point.z)

    return TestPattern()


class TestPatterns:
    def test_create_stripe_pattern(self):
        pattern = StripePattern(Color.white(), Color.black())
        assert pattern.first_color == Color.white()
        assert pattern.second_color == Color.black()

    def test_stripe_pattern_constant_in_y(self):
        pattern = StripePattern(Color.white(), Color.black())
        assert pattern.pattern_at(Point(0, 0, 0)) == Color.white()
        assert pattern.pattern_at(Point(0, 1, 0)) == Color.white()
        assert pattern.pattern_at(Point(0, 2, 0)) == Color.white()

    def test_stripe_pattern_constant_in_z(self):
        pattern = StripePattern(Color.white(), Color.black())
        assert pattern.pattern_at(Point(0, 0, 0)) == Color.white()
        assert pattern.pattern_at(Point(0, 0, 1)) == Color.white()
        assert pattern.pattern_at(Point(0, 0, 2)) == Color.white()

    def test_stripe_pattern_alternates_in_x(self):
        pattern = StripePattern(Color.white(), Color.black())
        assert pattern.pattern_at(Point(0, 0, 0)) == Color.white()
        assert pattern.pattern_at(Point(0.9, 0, 0)) == Color.white()
        assert pattern.pattern_at(Point(1, 0, 0)) == Color.black()
        assert pattern.pattern_at(Point(-0.1, 0, 0)) == Color.black()
        assert pattern.pattern_at(Point(-1, 0, 0)) == Color.black()
        assert pattern.pattern_at(Point(-1.1, 0, 0)) == Color.white()

    def test_pattern_with_object_transformation(self):
        obj = Sphere()
        obj.transformation = scaling(2, 2, 2)
        pattern = test_pattern()
        c = pattern.pattern_at_shape(obj, Point(2, 3, 4))
        assert c == Color(1, 1.5, 2)

    def test_pattern_with_pattern_transformation(self):
        obj = Sphere()
        pattern = test_pattern()
        pattern.transformation = scaling(2, 2, 2)
        c = pattern.pattern_at_shape(obj, Point(2, 3, 4))
        assert c == Color(1, 1.5, 2)

    def test_pattern_with_both_object_and_pattern_transformation(self):
        obj = Sphere()
        obj.transformation = scaling(2, 2, 2)
        pattern = test_pattern()
        pattern.transformation = translation(0.5, 1, 1.5)
        c = pattern.pattern_at_shape(obj, Point(2.5, 3, 3.5))
        assert c == Color(0.75, 0.5, 0.25)

    def test_default_pattern_transformation(self):
        pattern = test_pattern()
        assert pattern.transformation == Matrix.identity()

    def test_assign_transformation(self):
        pattern = test_pattern()
        pattern.transformation = translation(1, 2, 3)
        assert pattern.transformation == translation(1, 2, 3)



