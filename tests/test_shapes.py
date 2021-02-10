from math import sqrt, pi

import pytest

from raytracer.matrices import translation, scaling, rotation_z, rotation_y, rotation_x
from raytracer.shapes import *
from raytracer.tuples import Vector, Point


def test_shape():
    class TestShape(Shape):
        def __init__(self):
            super().__init__()
            self.saved_ray = None

        def _local_intersect(self, ray: Ray):
            self.saved_ray = ray
            return Intersections()

        def _local_normal_at(self, point: Point, hit: Intersection = None) -> Vector:
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

    def test_group_has_bounding_box_containing_its_children(self):
        s = Sphere()
        s.transformation = translation(2, 5, -3) * scaling(2, 2, 2)
        c = Cylinder()
        c.minimum = -2
        c.maximum = 2
        c.transformation = translation(-4, -1, 4) * scaling(0.5, 1, 0.5)
        group = Group()
        group.add_children(s, c)

        box = group.bounds()
        assert box.minimum == Point(-4.5, -3, -5)
        assert box.maximum == Point(4, 7, 4.5)


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

    @pytest.mark.parametrize("point, result", [(Point(5, -2, 0), True),
                                               (Point(11, 4, 7), True),
                                               (Point(8, 1, 3), True),
                                               (Point(3, 0, 3), False),
                                               (Point(8, -4, 3), False),
                                               (Point(8, 1, -1), False),
                                               (Point(13, 1, 3), False),
                                               (Point(8, 5, 3), False),
                                               (Point(8, 1, 8), False)])
    def test_check_box_contains_given_point(self, point, result):
        box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
        assert box.contains_point(point) is result

    @pytest.mark.parametrize("minimum, maximum, result", [(Point(5, -2, 0), Point(11, 4, 7), True),
                                                  (Point(6, -1, 1), Point(10, 3, 6), True),
                                                  (Point(4, -3, 1), Point(10, 3, 6), False),
                                                  (Point(6, -1, 1), Point(12, 5, 8), False)])
    def test_check_box_contains_given_box(self, minimum, maximum, result):
        box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
        box2 = BoundingBox(minimum, maximum)
        assert box.contains_box(box2) is result

    def test_transforming_bounding_box(self):
        box = BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))
        box2 = box.transform(rotation_x(pi / 4) * rotation_y(pi / 4))
        assert box2.minimum == Point(-1.41421, -1.70711, -1.70711)
        assert box2.maximum == Point(1.41421, 1.70711, 1.70711)

    def test_query_shape_bounding_box_in_parent_space(self):
        s = Sphere()
        s.transformation = translation(1, -3, 5) * scaling(0.5, 2, 4)
        box = s.parent_space_bounds()
        assert box.minimum == Point(0.5, -5, 1)
        assert box.maximum == Point(1.5, -1, 9)

    @pytest.mark.parametrize("origin, direction, result", [(Point(5, 0.5, 0), Vector(-1, 0, 0), True),
                                                           (Point(-5, 0.5, 0), Vector(1, 0, 0), True),
                                                           (Point(0.5, 5, 0), Vector(0, -1, 0), True),
                                                           (Point(0.5, -5, 0), Vector(0, 1, 0), True),
                                                           (Point(0.5, 0, 5), Vector(0, 0, -1), True),
                                                           (Point(0.5, 0, -5), Vector(0, 0, 1), True),
                                                           (Point(0, 0.5, 0), Vector(0, 0, 1), True),
                                                           (Point(-2, 0, 0), Vector(2, 4, 6), False),
                                                           (Point(0, -2, 0), Vector(6, 2, 4), False),
                                                           (Point(0, 0, -2), Vector(4, 6, 2), False),
                                                           (Point(2, 0, 2), Vector(0, 0, -1), False),
                                                           (Point(0, 2, 2), Vector(0, -1, 0), False),
                                                           (Point(2, 2, 0), Vector(-1, 0, 0), False)])
    def test_intersect_ray_with_bounding_box_at_origin(self, origin, direction, result):
        box = BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = box.intersect(r)
        assert (xs.count > 0) is result

    @pytest.mark.parametrize("origin, direction, result", [(Point(15, 1, 2), Vector(-1, 0, 0), True),
                                                           (Point(-5, -1, 4), Vector(1, 0, 0), True),
                                                           (Point(7, 6, 5), Vector(0, -1, 0), True),
                                                           (Point(9, -5, 6), Vector(0, 1, 0), True),
                                                           (Point(8, 2, 12), Vector(0, 0, -1), True),
                                                           (Point(6, 0, -5), Vector(0, 0, 1), True),
                                                           (Point(8, 1, 3.5), Vector(0, 0, 1), True),
                                                           (Point(9, -1, -8), Vector(2, 4, 6), False),
                                                           (Point(8, 3, -4), Vector(6, 2, 4), False),
                                                           (Point(9, -1, -2), Vector(4, 6, 2), False),
                                                           (Point(4, 0, 9), Vector(0, 0, -1), False),
                                                           (Point(8, 6, -1), Vector(0, -1, 0), False),
                                                           (Point(12, 5, 4), Vector(-1, 0, 0), False)])
    def test_intersect_ray_with_non_cubic_bounding_box(self, origin, direction, result):
        box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
        norm_direction = direction.normalize()
        r = Ray(origin, norm_direction)
        xs = box.intersect(r)
        assert (xs.count > 0) is result

    def test_intersect_ray_group_doesnt_test_children_if_box_is_missed(self):
        child = test_shape()
        g = Group()
        g.add_children(child)
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        xs = g.intersect(r)
        assert not child.saved_ray

    def test_intersect_ray_group_test_children_if_box_is_hit(self):
        child = test_shape()
        g = Group()
        g.add_children(child)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = g.intersect(r)
        assert child.saved_ray


class TestTriangles:
    def test_constructing_triangle(self):
        p1 = Point(0, 1, 0)
        p2 = Point(-1, 0, 0)
        p3 = Point(1, 0, 0)
        t = Triangle(p1, p2, p3)
        assert t.p1 == p1
        assert t.p2 == p2
        assert t.p3 == p3
        assert t.e1 == Vector(-1, -1, 0)
        assert t.e2 == Vector(1, -1, 0)
        assert t.normal == Vector(0, 0, -1)

    def test_finding_normal_on_triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        n1 = t._local_normal_at(Point(0, 0.5, 0))
        n2 = t._local_normal_at(Point(-0.5, 0.75, 0))
        n3 = t._local_normal_at(Point(0.5, 0.25, 0))
        assert n1 == t.normal
        assert n2 == t.normal
        assert n3 == t.normal

    def test_triangle_has_bounded_box(self):
        p1 = Point(-3, 7, 2)
        p2 = Point(6, 2, -4)
        p3 = Point(2, -1, -1)
        t = Triangle(p1, p2, p3)
        box = t.bounds()
        assert box.minimum == Point(-3, -1, -4)
        assert box.maximum == Point(6, 7, 2)

    def test_intersect_ray_parallel_to_triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, -1, -2), Vector(0, 1, 0))
        xs = t._local_intersect(r)
        assert xs.count == 0

    def test_ray_misses_p1_p3_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(1, 1, -2), Vector(0, 0, 1))
        xs = t._local_intersect(r)
        assert xs.count == 0

    def test_ray_misses_p1_p2_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(-1, 1, -2), Vector(0, 0, 1))
        xs = t._local_intersect(r)
        assert xs.count == 0

    def test_ray_misses_p2_p3_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, -1, -2), Vector(0, 0, 1))
        xs = t._local_intersect(r)
        assert xs.count == 0

    def test_ray_strikes_triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, 0.5, -2), Vector(0, 0, 1))
        xs = t._local_intersect(r)
        assert xs.count == 1
        assert xs[0].t == 2


def smooth_triangle():
    p1, p2, p3 = Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0)
    n1, n2, n3 = Vector(0, 1, 0), Vector(-1, 0, 0), Vector(1, 0, 0)
    return SmoothTriangle(p1, p2, p3, n1, n2, n3)


class TestSmoothTriangles:
    def test_constructing_smooth_triangle(self):
        t = smooth_triangle()
        assert t.p1 == Point(0, 1, 0)
        assert t.p2 == Point(-1, 0, 0)
        assert t.p3 == Point(1, 0, 0)
        assert t.n1 == Vector(0, 1, 0)
        assert t.n2 == Vector(-1, 0, 0)
        assert t.n3 == Vector(1, 0, 0)

    def test_intersection_with_smooth_triangle_stores_u_and_v(self):
        t = smooth_triangle()
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = t._local_intersect(r)
        assert xs[0].u == pytest.approx(0.45, EPSILON)
        assert xs[0].v == pytest.approx(0.25, EPSILON)

    def test_smooth_triangle_uses_u_v_to_interpolate_the_normal(self):
        t = smooth_triangle()
        i = Intersection(1, t, 0.45, 0.25)
        n = t.normal_at(Point(0, 0, 0), i)
        assert n == Vector(-0.5547, 0.83205, 0)

    def test_preparing_normal_on_smooth_triangle(self):
        t = smooth_triangle()
        x = Intersection(1, t, 0.45, 0.25)
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = Intersections(x)
        comps = x.prepare_computations(r, xs)
        assert comps.normalv == Vector(-0.5547, 0.83205, 0)

