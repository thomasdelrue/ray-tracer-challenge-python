from math import sqrt
from raytracer.tuples import Tuple, TupleType, Point, Vector, dot, cross, Color


class TestTuples:
    def test_tuple_is_a_point(self):
        a = Tuple(4.3, -4.2, 3.1, 1.0)
        assert a.x == 4.3
        assert a.y == -4.2
        assert a.z == 3.1
        assert a.w == 1.0
        assert a.type == TupleType.POINT.name
        assert a.type != TupleType.VECTOR.name

    def test_tuple_is_a_vector(self):
        a = Tuple(4.3, -4.2, 3.1, 0.0)
        assert a.x == 4.3
        assert a.y == -4.2
        assert a.z == 3.1
        assert a.w == 0.0
        assert a.type != TupleType.POINT.name
        assert a.type == TupleType.VECTOR.name

    def test_point_creates_tuple_w_1(self):
        p = Point(4, -4, 3)
        assert p == Tuple(4, -4, 3, 1.0)

    def test_vector_creates_tuple_w_0(self):
        v = Vector(4, -4, 3)
        assert v == Tuple(4, -4, 3, 0.0)

    def test_compare_2_points_for_equality(self):
        p1 = Point(4, -4, 3)
        p2 = Point(4, -4, 3)
        assert p1 == p2
        assert p1 is not p2

    def test_adding_two_tuples(self):
        a1 = Tuple(3, -2, 5, 1)
        a2 = Tuple(-2, 3, 1, 0)
        assert a1 + a2 == Tuple(1, 1, 6, 1)

    def test_subtract_two_points(self):
        p1 = Point(3, 2, 1)
        p2 = Point(5, 6, 7)
        assert p1 - p2 == Vector(-2, -4, -6)

    def test_subtract_vector_from_point(self):
        p = Point(3, 2, 1)
        v = Vector(5, 6, 7)
        assert p - v == Point(-2, -4, -6)

    def test_subtract_two_vectors(self):
        v1 = Point(3, 2, 1)
        v2 = Point(5, 6, 7)
        assert v1 - v2 == Vector(-2, -4, -6)

    def test_subtract_vector_from_zero_vector(self):
        zero = Vector(0, 0, 0)
        v = Vector(1, -2, 3)
        assert zero - v == Vector(-1, 2, -3)

    def test_negate_tuple(self):
        a = Tuple(1, -2, 3, -4)
        assert -a == Tuple(-1, 2, -3, 4)

    def test_multiply_tuple_by_scalar(self):
        a = Tuple(1, -2, 3, -4)
        assert a * 3.5 == Tuple(3.5, -7, 10.5, -14)

    def test_multiply_tuple_by_fraction(self):
        a = Tuple(1, -2, 3, -4)
        assert a * 0.5 == Tuple(0.5, -1, 1.5, -2)

    def test_divide_tuple_by_scalar(self):
        a = Tuple(1, -2, 3, -4)
        assert a / 2 == Tuple(0.5, -1, 1.5, -2)

    def test_magnitude(self):
        v = Vector(1, 0, 0)
        assert v.magnitude == 1

    def test_magnitude2(self):
        v = Vector(0, 1, 0)
        assert v.magnitude == 1

    def test_magnitude3(self):
        v = Vector(0, 0, 1)
        assert v.magnitude == 1

    def test_magnitude4(self):
        v = Vector(1, 2, 3)
        assert v.magnitude == sqrt(14)

    def test_magnitude5(self):
        v = Vector(-1, -2, -3)
        assert v.magnitude == sqrt(14)

    def test_normalize(self):
        v = Vector(4, 0, 0)
        assert v.normalize() == Vector(1, 0, 0)

    def test_normalize2(self):
        v = Vector(1, 2, 3)
        assert v.normalize() == Vector(0.26726, 0.53452, 0.80178)

    def test_magnitude_of_normalized_vector(self):
        v = Vector(1, 2, 3)
        assert v.normalize().magnitude == 1

    def test_dot_product_of_two_tuples(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        assert dot(a, b) == 20

    def test_cross_product_of_two_vectors(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        assert cross(a, b) == Vector(-1, 2, -1)
        assert cross(b, a) == Vector(1, -2, 1)

    def test_colors_are_rgb_tuples(self):
        c = Color(-0.5, 0.4, 1.7)
        assert c.red == -0.5
        assert c.green == 0.4
        assert c.blue == 1.7

    def test_add_colors(self):
        c1 = Color(0.9, 0.6, 0.75)
        c2 = Color(0.7, 0.1, 0.25)
        assert c1 + c2 == Color(1.6, 0.7, 1.0)

    def test_subtract_colors(self):
        c1 = Color(0.9, 0.6, 0.75)
        c2 = Color(0.7, 0.1, 0.25)
        assert c1 - c2 == Color(0.2, 0.5, 0.5)

    def test_multiply_color_by_scalar(self):
        c = Color(0.2, 0.3, 0.4)
        assert c * 2 == Color(0.4, 0.6, 0.8)
        assert 2 * c == Color(0.4, 0.6, 0.8)

    def test_multiply_colors(self):
        c1 = Color(1, 0.2, 0.4)
        c2 = Color(0.9, 1, 0.1)
        assert c1 * c2 == Color(0.9, 0.2, 0.04)

    def test_reflect_vector_at_45(self):
        v = Vector(1, -1, 0)
        n = Vector(0, 1, 0)
        r = v.reflect(n)
        assert r == Vector(1, 1, 0)

    def test_reflect_vector_at_slanted_surface(self):
        v = Vector(0, -1, 0)
        n = Vector(sqrt(2) / 2, sqrt(2) / 2, 0)
        r = v.reflect(n)
        assert r == Vector(1, 0, 0)


