from math import sqrt, pi

import pytest

from raytracer.matrices import translation, scaling, rotation_z, rotation_y
from raytracer.shapes import *
from raytracer.tuples import Vector, Point


def test_shape():
    class TestShape(Shape):
        def _local_intersect(self, ray: Ray):
            self.saved_ray = ray

        def _local_normal_at(self, point: Point) -> Vector:
            return Vector(point.x, point.y, point.z)

        def bounds(self) -> BoundingBox:
            return BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))

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

    def test_shape_has_bounds(self):
        s = test_shape()
        box = s.bounds()
        assert box.minimum == Point(-1, -1, -1)
        assert box.maximum == Point(1, 1, 1)


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

    def test_normal_sphere_at_non_axial_point(self):
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

    def test_sphere_has_bounding_box(self):
        s = Sphere()
        box = s.bounds()
        assert box.minimum == Point(-1, -1, -1)
        assert box.maximum == Point(1, 1, 1)


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

    def test_plane_has_bounding_box(self):
        p = Plane()
        box = p.bounds()
        x, y, z, _ = box.minimum
        assert (x, y, z) == (-INF, 0, -INF)
        x, y, z, _ = box.maximum
        assert (x, y, z) == (INF, 0, INF)


class TestCubes:
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

    def test_cube_has_bounding_box(self):
        c = Cube()
        box = c.bounds()
        assert box.minimum == Point(-1, -1, -1)
        assert box.maximum == Point(1, 1, 1)


class TestCylinders:
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
        assert c.minimum == -INF
        assert c.maximum == INF

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

    @pytest.mark.parametrize("point, normal", [(Point(0, 1, 0), Vector(0, -1, 0)),
                                               (Point(0.5, 1, 0), Vector(0, -1, 0)),
                                               (Point(0, 1, 0.5), Vector(0, -1, 0)),
                                               (Point(0, 2, 0), Vector(0, 1, 0)),
                                               (Point(0.5, 2, 0), Vector(0, 1, 0)),
                                               (Point(0, 2, 0.5), Vector(0, 1, 0))])
    def test_normal_vector_on_cylinders_end_caps(self, point, normal):
        c = Cylinder(closed=True)
        c.minimum = 1
        c.maximum = 2
        n = c._local_normal_at(point)
        assert n == normal

    def test_unbounded_cylinder_has_bounding_box(self):
        c = Cylinder()
        box = c.bounds()
        x, y, z, _ = box.minimum
        assert (x, y, z) == (-1, -INF, -1)
        x, y, z, _ = box.maximum
        assert (x, y, z) == (1, INF, 1)

    def test_bounded_cylinder_has_bounding_box(self):
        c = Cylinder()
        c.minimum = -5
        c.maximum = 3
        box = c.bounds()
        assert box.minimum == Point(-1, -5, -1)
        assert box.maximum == Point(1, 3, 1)


class TestCones:
    @pytest.mark.parametrize("origin, direction, t0, t1", [(Point(0, 0, -5), Vector(0, 0, 1), 5, 5),
                                                           (Point(0, 0, -5), Vector(1, 1, 1), 8.66025, 8.66025),
                                                           (Point(1, 1, -5), Vector(-0.5, -1, 1), 4.55006, 49.44994)])
    def test_intersect_cone_with_ray(self, origin, direction, t0, t1):
        shape = Cone()
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = shape._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == pytest.approx(t0, EPSILON)
        assert xs[1].t == pytest.approx(t1, EPSILON)

    def test_intersecting_cone_with_ray_parallel_to_one_of_halves(self):
        shape = Cone()
        norm_direction = Vector(0, 1, 1).normalize()
        r = Ray(Point(0, 0, -1), norm_direction)
        xs = shape._local_intersect(r)
        assert xs.count == 1
        assert xs[0].t == pytest.approx(0.35355, EPSILON)

    @pytest.mark.parametrize("origin, direction, count", [(Point(0, 0, -5), Vector(0, 1, 0), 0),
                                                          (Point(0, 0, -0.25), Vector(0, 1, 1), 2),
                                                          (Point(0, 0, -0.25), Vector(0, 1, 0), 4)])
    def test_intersecting_cone_end_caps(self, origin, direction, count):
        shape = Cone(closed=True)
        shape.minimum = -0.5
        shape.maximum = 0.5
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = shape._local_intersect(r)
        assert xs.count == count

    @pytest.mark.parametrize("point, normal", [(Point(0, 0, 0), Vector(0, 0, 0)),
                                               (Point(1, 1, 1), Vector(1, -sqrt(2), 1)),
                                               (Point(-1, -1, 0), Vector(-1, 1, 0))])
    def test_normal_vector_on_cone(self, point, normal):
        shape = Cone()
        n = shape._local_normal_at(point)
        assert n == normal

    def test_unbounded_cone_has_bounding_box(self):
        c = Cone()
        box = c.bounds()
        x, y, z, _ = box.minimum
        assert (x, y, z) == (-INF, -INF, -INF)
        x, y, z, _ = box.maximum
        assert (x, y, z) == (INF, INF, INF)

    def test_bounded_cone_has_bounding_box(self):
        c = Cone()
        c.minimum = -5
        c.maximum = 3
        box = c.bounds()
        assert box.minimum == Point(-5, -5, -5)
        assert box.maximum == Point(5, 3, 5)


class TestGroups:
    def test_create_new_group(self):
        g = Group()
        assert g.transformation == Matrix.identity()
        assert g.empty

    def test_shape_has_parent_attribute(self):
        s = test_shape()
        assert s.parent is None

    def test_adding_child_to_group(self):
        g = Group()
        s = test_shape()
        g.add_children(s)
        assert not g.empty
        assert s in g
        assert s.parent == g

    def test_intersect_ray_with_empty_group(self):
        g = Group()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        xs = g._local_intersect(r)
        assert xs.count == 0

    def test_intersect_ray_with_non_empty_group(self):
        g = Group()
        s1 = Sphere()
        s2 = Sphere()
        s2.transformation = translation(0, 0, -3)
        s3 = Sphere()
        s3.transformation = translation(5, 0, 0)
        g.add_children(s1, s2, s3)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = g._local_intersect(r)
        assert xs.count == 4
        assert xs[0].object == s2
        assert xs[1].object == s2
        assert xs[2].object == s1
        assert xs[3].object == s1

    def test_intersect_transformed_group(self):
        g = Group()
        g.transformation = scaling(2, 2, 2)
        s = Sphere()
        s.transformation = translation(5, 0, 0)
        g.add_children(s)
        r = Ray(Point(10, 0, -10), Vector(0, 0, 1))
        xs = g.intersect(r)
        assert xs.count == 2

    def test_convert_point_from_world_to_object_space(self):
        g1 = Group()
        g1.transformation = rotation_y(pi / 2)
        g2 = Group()
        g2.transformation = scaling(2, 2, 2)
        g1.add_children(g2)

        s = Sphere()
        s.transformation = translation(5, 0, 0)
        g2.add_children(s)
        p = s.world_to_object(Point(-2, 0, -10))
        assert p == Point(0, 0, -1)

    def test_convert_normal_from_object_to_world_space(self):
        g1 = Group()
        g1.transformation = rotation_y(pi / 2)
        g2 = Group()
        g2.transformation = scaling(1, 2, 3)
        g1.add_children(g2)

        s = Sphere()
        s.transformation = translation(5, 0, 0)
        g2.add_children(s)
        n = s.normal_to_world(Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
        assert n == Vector(0.28571, 0.42857, -0.85714)

    def test_find_normal_on_child_object(self):
        g1 = Group()
        g1.transformation = rotation_y(pi / 2)
        g2 = Group()
        g2.transformation = scaling(1, 2, 3)
        g1.add_children(g2)

        s = Sphere()
        s.transformation = translation(5, 0, 0)
        g2.add_children(s)
        n = s.normal_at(Point(1.7321, 1.1547, -5.5774))
        assert n == Vector(0.28570, 0.42854, -0.85716)


class TestBoundingBoxes:
    def test_create_empty_bounding_box(self):
        box = BoundingBox()
        x, y, z, _ = box.minimum
        assert (x, y, z) == (INF, INF, INF)
        x, y, z, _ = box.maximum
        assert (x, y, z) == (-INF, -INF, -INF)

    def test_create_bounding_box_with_volume(self):
        box = BoundingBox(Point(-1, -2, -3), Point(3, 2, 1))
        assert box.minimum == Point(-1, -2, -3)
        assert box.maximum == Point(3, 2, 1)

    def test_adding_points_to_empty_bounding_box(self):
        box = BoundingBox()
        p1 = Point(-5, 2, 0)
        p2 = Point(7, 0, -3)
        box.include(p1)
        box.include(p2)
        assert box.minimum == Point(-5, 0, -3)
        assert box.maximum == Point(7, 2, 0)

    def test_merge_bounding_box_in_another(self):
        box1 = BoundingBox(Point(-5, -2, 0), Point(7, 4, 4))
        box2 = BoundingBox(Point(8, -7, -2), Point(14, 2, 8))
        box1.merge(box2)
        assert box1.minimum == Point(-5, -7, -2)
        assert box1.maximum == Point(14, 4, 8)
