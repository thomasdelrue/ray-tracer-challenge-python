from math import sqrt, pi
from raytracer import EPSILON
from raytracer.materials import Material
from raytracer.matrices import Matrix, translation, scaling, rotation_z
from raytracer.rays import Ray
from raytracer.shapes import Shape, Sphere, Plane, Cube, Cylinder
from raytracer.tuples import Vector, Point
import pytest


def test_shape():
    class TestShape(Shape):
        def _local_intersect(self, ray: Ray):
            self.saved_ray = ray

        def _local_normal_at(self, point: Point) -> Vector:
            return Vector(point.x, point.y, point.z)

    return TestShape()


class TestShapes:
    def test_default_transformation(self):
        s = test_shape()
        assert s.transformation == Matrix.identity()

    def test_change_transformation(self):
        s = test_shape()
        t = translation(2, 3, 4)
        s.transformation = t
        assert s.transformation == t

    def test_default_material(self):
        s = test_shape()
        m = s.material
        assert m == Material()

    def test_change_material(self):
        s = test_shape()
        m = Material()
        m.ambient = 1
        s.material = m
        assert s.material == m

    def test_intersecting_scaled_shape_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = test_shape()
        s.transformation = scaling(2, 2, 2)
        _ = s.intersect(r)
        assert s.saved_ray.origin == Point(0, 0, -2.5)
        assert s.saved_ray.direction == Vector(0, 0, 0.5)

    def test_intersecting_translated_shape_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = test_shape()
        s.transformation = translation(5, 0, 0)
        _ = s.intersect(r)
        assert s.saved_ray.origin == Point(-5, 0, -5)
        assert s.saved_ray.direction == Vector(0, 0, 1)

    def test_compute_normal_on_translated_shape(self):
        s = test_shape()
        s.transformation = translation(0, 1, 0)
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        assert n == Vector(0, 0.70711, -0.70711)

    def test_compute_normal_on_transformed_shape(self):
        s = test_shape()
        s.transformation = scaling(1, 0.5, 1) * rotation_z(pi / 5)
        n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))
        assert n == Vector(0, 0.97014, -0.24254)


class TestSpheres:
    def test_ray_intersects_sphere_at_two_points(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == 4.0
        assert xs[1].t == 6.0

    def test_ray_intersects_sphere_at_tangent(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == 5.0
        assert xs[1].t == 5.0

    def test_ray_misses_sphere(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 0

    def test_ray_originates_inside_sphere(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == -1.0
        assert xs[1].t == 1.0

    def test_sphere_is_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == -6.0
        assert xs[1].t == -4.0

    def test_intersect_sets_object_on_the_intersection(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s._local_intersect(r)
        assert xs.count == 2
        assert xs[0].object == s
        assert xs[1].object == s

    def test_normal_sphere_at_point_on_x_axis(self):
        s = Sphere()
        n = s._local_normal_at(Point(1, 0, 0))
        assert n == Vector(1, 0, 0)

    def test_normal_sphere_at_point_on_y_axis(self):
        s = Sphere()
        n = s._local_normal_at(Point(0, 1, 0))
        assert n == Vector(0, 1, 0)

    def test_normal_sphere_at_point_on_z_axis(self):
        s = Sphere()
        n = s._local_normal_at(Point(0, 0, 1))
        assert n == Vector(0, 0, 1)

    def test_normal_sphere_at_nonaxial_point(self):
        s = Sphere()
        n = s._local_normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
        assert n == Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)

    def test_normal_is_normalized_vector(self):
        s = Sphere()
        n = s._local_normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
        assert n == n.normalize()

    def test_sphere_is_a_shape(self):
        s = Sphere()
        assert isinstance(s, Shape)


class TestPlanes:
    def test_normal_of_plane_is_constant_everywhere(self):
        p = Plane()
        n1 = p._local_normal_at(Point(0, 0, 0))
        n2 = p._local_normal_at(Point(10, 0, -10))
        n3 = p._local_normal_at(Point(-5, 0, 150))
        assert n1 == Vector(0, 1, 0)
        assert n2 == Vector(0, 1, 0)
        assert n3 == Vector(0, 1, 0)

    def test_intersect_with_ray_parallel_to_plan(self):
        p = Plane()
        r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
        xs = p._local_intersect(r)
        assert xs.count == 0

    def test_intersect_with_coplanar_ray(self):
        p = Plane()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        xs = p._local_intersect(r)
        assert xs.count == 0

    def test_intersect_plane_from_above(self):
        p = Plane()
        r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
        xs = p._local_intersect(r)
        assert xs.count == 1
        assert xs[0].t == 1
        assert xs[0].object == p

    def test_intersect_plane_from_below(self):
        p = Plane()
        r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
        xs = p._local_intersect(r)
        assert xs.count == 1
        assert xs[0].t == 1
        assert xs[0].object == p

    @pytest.mark.parametrize("point, normal", [(Point(1, 0.5, -0.8), Vector(1, 0, 0)),
                                              (Point(-1, -0.2, 0.9), Vector(-1, 0, 0)),
                                              (Point(-0.4, 1, -0.1), Vector(0, 1, 0)),
                                              (Point(0.3, -1, -0.7), Vector(0, -1, 0)),
                                              (Point(-0.6, 0.3, 1), Vector(0, 0, 1)),
                                              (Point(0.4, 0.4, -1), Vector(0, 0, -1)),
                                              (Point(1, 1, 1), Vector(1, 0, 0)),
                                              (Point(-1, -1, -1), Vector(-1, 0, 0))])
    def test_normal_on_surface_of_cube(self, point, normal):
        c = Cube()
        p = point
        result = c._local_normal_at(p)
        assert result == normal

    @pytest.mark.parametrize("origin, direction", [(Point(1, 0, 0), Vector(0, 1, 0)),
                                                  (Point(0, 0, 0), Vector(0, 1, 0)),
                                                  (Point(0, 0, -5), Vector(1, 1, 1))])
    def test_ray_misses_cylinder(self, origin, direction):
        c = Cylinder()
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = c._local_intersect(r)
        assert xs.count == 0

    @pytest.mark.parametrize("origin, direction, t0, t1", [(Point(1, 0, -5), Vector(0, 0, 1), 5, 5),
                                                          (Point(0, 0, -5), Vector(0, 0, 1), 4, 6),
                                                          (Point(0.5, 0, -5), Vector(0.1, 1, 1), 6.80798, 7.08872)])
    def test_ray_strikes_cylinder(self, origin, direction, t0, t1):
        c = Cylinder()
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = c._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == pytest.approx(t0, EPSILON)
        assert xs[1].t == pytest.approx(t1, EPSILON)

    @pytest.mark.parametrize("point, normal", [(Point(1, 0, 0), Vector(1, 0, 0)),
                                               (Point(0, 5, -1), Vector(0, 0, -1)),
                                               (Point(0, -2, 1), Vector(0, 0, 1)),
                                               (Point(-1, 1, 0), Vector(-1, 0, 0))])
    def test_normal_on_cylinder(self, point, normal):
        c = Cylinder()
        n = c._local_normal_at(point)
        assert n == normal

    def test_default_min_and_max_for_cylinder(self):
        c = Cylinder()
        assert c.minimum == float('-inf')
        assert c.maximum == float('inf')

    @pytest.mark.parametrize("point, direction, count", [(Point(0, 1.5, 0), Vector(0.1, 1, 0), 0),
                                                         (Point(0, 3, -5), Vector(0, 0, 1), 0),
                                                         (Point(0, 0, -5), Vector(0, 0, 1), 0),
                                                         (Point(0, 2, -5), Vector(0, 0, 1), 0),
                                                         (Point(0, 1, -5), Vector(0, 0, 1), 0),
                                                         (Point(0, 1.5, -5), Vector(0, 0, 1), 2)])
    def test_intersecting_constrained_cylinder(self, point, direction, count):
        c = Cylinder()
        c.minimum = 1
        c.maximum = 2
        norm_direction = direction.normalize()
        r = Ray(point, norm_direction)
        xs = c._local_intersect(r)
        assert xs.count == count

    def test_default_closed_value_for_cylinder(self):
        c = Cylinder()
        assert not c.closed

    @pytest.mark.parametrize("point, direction, count", [(Point(0, 3, 0), Vector(0, -1, 0), 2),
                                                         (Point(0, 3, -2), Vector(0, -1, 2), 2),
                                                         (Point(0, 4, -2), Vector(0, -1, 1), 2),
                                                         (Point(0, 0, -2), Vector(0, 1, 2), 2),
                                                         (Point(0, -1, -2), Vector(0, 1, 1), 2)])
    def test_intersecting_caps_of_closed_cylinder(self, point, direction, count):
        c = Cylinder(closed=True)
        c.minimum = 1
        c.maximum = 2
        norm_direction = direction.normalize()
        r = Ray(point, norm_direction)
        xs = c._local_intersect(r)
        assert xs.count == count
        assert c.closed

