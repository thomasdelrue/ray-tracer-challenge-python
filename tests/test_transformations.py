from raytracer.matrices import translation, scaling, rotation_x, rotation_y, rotation_z, shearing
from raytracer.tuples import Point, Vector
import math


class TestTransformations:
    def test_multiply_by_translation_matrix(self):
        transform = translation(5, -3, 2)
        p = Point(-3, 4, 5)
        assert transform * p == Point(2, 1, 7)

    def test_multiply_by_inverse_of_translation_matrix(self):
        transform = translation(5, -3, 2)
        inv = transform.inverse()
        p = Point(-3, 4, 5)
        assert inv * p == Point(-8, 7, 3)

    def test_translation_does_not_affect_vectors(self):
        transform = translation(5, -3, 2)
        v = Vector(-3, 4, 5)
        assert transform * v == v

    def test_scaling_matrix_applied_to_point(self):
        transform = scaling(2, 3, 4)
        p = Point(-4, 6, 8)
        assert transform * p == Point(-8, 18, 32)

    def test_scaling_matrix_applied_to_vector(self):
        transform = scaling(2, 3, 4)
        v = Vector(-4, 6, 8)
        assert transform * v == Vector(-8, 18, 32)

    def test_multiply_by_inverse_of_scaling_matrix(self):
        transform = scaling(2, 3, 4)
        inv = transform.inverse()
        v = Vector(-4, 6, 8)
        assert inv * v == Vector(-2, 2, 2)

    def test_reflection_is_scaling_by_negative_value(self):
        transform = scaling(-1, 1, 1)
        p = Point(2, 3, 4)
        assert transform * p == Point(-2, 3, 4)

    def test_rotate_point_around_x_axis(self):
        p = Point(0, 1, 0)
        half_quarter = rotation_x(math.pi / 4)
        full_quarter = rotation_x(math.pi / 2)
        assert half_quarter * p == Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
        assert full_quarter * p == Point(0, 0, 1)

    def test_inverse_of_x_rotation_rotates_opposite_direction(self):
        p = Point(0, 1, 0)
        full_quarter = rotation_x(math.pi / 2)
        inv = full_quarter.inverse()
        assert inv * p == Point(0, 0, -1)

    def test_rotate_point_around_y_axis(self):
        p = Point(0, 0, 1)
        half_quarter = rotation_y(math.pi / 4)
        full_quarter = rotation_y(math.pi / 2)
        assert half_quarter * p == Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
        assert full_quarter * p == Point(1, 0, 0)

    def test_rotate_point_around_z_axis(self):
        p = Point(0, 1, 0)
        half_quarter = rotation_z(math.pi / 4)
        full_quarter = rotation_z(math.pi / 2)
        assert half_quarter * p == Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0)
        assert full_quarter * p == Point(-1, 0, 0)

    def test_shear_moves_x_in_proportion_to_y(self):
        transform = shearing(1, 0, 0, 0, 0, 0)
        p = Point(2, 3, 4)
        assert transform * p == Point(5, 3, 4)

    def test_shear_moves_x_in_proportion_to_z(self):
        transform = shearing(0, 1, 0, 0, 0, 0)
        p = Point(2, 3, 4)
        assert transform * p == Point(6, 3, 4)

    def test_shear_moves_y_in_proportion_to_x(self):
        transform = shearing(0, 0, 1, 0, 0, 0)
        p = Point(2, 3, 4)
        assert transform * p == Point(2, 5, 4)

    def test_shear_moves_y_in_proportion_to_z(self):
        transform = shearing(0, 0, 0, 1, 0, 0)
        p = Point(2, 3, 4)
        assert transform * p == Point(2, 7, 4)

    def test_shear_moves_z_in_proportion_to_x(self):
        transform = shearing(0, 0, 0, 0, 1, 0)
        p = Point(2, 3, 4)
        assert transform * p == Point(2, 3, 6)

    def test_shear_moves_z_in_proportion_to_y(self):
        transform = shearing(0, 0, 0, 0, 0, 1)
        p = Point(2, 3, 4)
        assert transform * p == Point(2, 3, 7)

    def test_individual_transformations_in_sequence(self):
        p = Point(1, 0, 1)
        a = rotation_x(math.pi / 2)
        b = scaling(5, 5, 5)
        c = translation(10, 5, 7)
        p2 = a * p
        assert p2 == Point(1, -1, 0)
        p3 = b * p2
        assert p3 == Point(5, -5, 0)
        p4 = c * p3
        assert p4 == Point(15, 0, 7)

    def test_chained_transformations_are_in_reverse_order(self):
        p = Point(1, 0, 1)
        a = rotation_x(math.pi / 2)
        b = scaling(5, 5, 5)
        c = translation(10, 5, 7)
        t = c * b * a * p
        assert t == Point(15, 0, 7)





