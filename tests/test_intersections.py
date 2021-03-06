from math import sqrt
import pytest
from raytracer import EPSILON
from raytracer.intersections import Intersection, Intersections
from raytracer.matrices import translation, scaling
from raytracer.rays import Ray
from raytracer.shapes import Sphere, Plane, Cube, Triangle
from raytracer.tuples import Point, Vector


class TestIntersections:
    @pytest.fixture
    def glass_sphere(self):
        def _create_glass_sphere():
            s = Sphere()
            s.material.transparency = 1.0
            s.material.refractive_index = 1.5
            return s
        return _create_glass_sphere

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

    def test_precomputing_state_of_intersection(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        assert comps.t == i.t
        assert comps.object == i.object
        assert comps.point == Point(0, 0, -1)
        assert comps.eyev == Vector(0, 0, -1)
        assert comps.normalv == Vector(0, 0, -1)

    def test_hit_when_intersection_occurs_on_outside(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        assert not comps.inside

    def test_hit_when_intersection_occurs_on_inside(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(1, shape)
        comps = i.prepare_computations(r)
        assert comps.point == Point(0, 0, 1)
        assert comps.eyev == Vector(0, 0, -1)
        assert comps.inside
        assert comps.normalv == Vector(0, 0, -1)

    def test_hit_should_offset_the_point(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        shape.transformation = translation(0, 0, 1)
        i = Intersection(5, shape)
        comps = i.prepare_computations(r)
        assert comps.over_point.z < -EPSILON / 2
        assert comps.point.z > comps.over_point.z

    def test_precompute_reflection_vector(self):
        shape = Plane()
        r = Ray(Point(0, 1, -1), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        i = Intersection(sqrt(2), shape)
        comps = i.prepare_computations(r)
        assert comps.reflectv == Vector(0, sqrt(2) / 2, sqrt(2) / 2)

    @pytest.mark.parametrize("index,n1,n2", [(0, 1.0, 1.5),
                                             (1, 1.5, 2.0),
                                             (2, 2.0, 2.5),
                                             (3, 2.5, 2.5),
                                             (4, 2.5, 1.5),
                                             (5, 1.5, 1.0)])
    def test_finding_n1_and_n2_at_various_intersections(self, glass_sphere, index, n1, n2):
        a = glass_sphere()
        a.transformation = scaling(2, 2, 2)
        a.material.refractive_index = 1.5
        b = glass_sphere()
        b.transformation = translation(0, 0, -0.25)
        b.material.refractive_index = 2.0
        c = glass_sphere()
        c.transformation = translation(0, 0, 0.25)
        c.material.refractive_index = 2.5
        r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
        xs = Intersections(Intersection(2, a), Intersection(2.75, b), Intersection(3.25, c),
                           Intersection(4.75, b), Intersection(5.25, c), Intersection(6, a))
        comps = xs[index].prepare_computations(r, xs)
        assert comps.n1 == n1
        assert comps.n2 == n2

    def test_under_point_is_offset_below_the_surface(self, glass_sphere):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = glass_sphere()
        shape.transformation = translation(0, 0, 1)
        i = Intersection(5, shape)
        xs = Intersections(i)
        comps = i.prepare_computations(r, xs)
        assert comps.under_point.z > EPSILON / 2
        assert comps.point.z < comps.under_point.z

    def test_schlick_approximation_under_total_internal_reflection(self, glass_sphere):
        shape = glass_sphere()
        r = Ray(Point(0, 0, sqrt(2) / 2), Vector(0, 1, 0))
        xs = Intersections(Intersection(-sqrt(2) / 2, shape), Intersection(sqrt(2) / 2, shape))
        comps = xs[1].prepare_computations(r, xs)
        reflectance = comps.schlick()
        assert reflectance == 1.0

    def test_schlick_approximation_with_perpendicular_viewing_angle(self, glass_sphere):
        shape = glass_sphere()
        r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
        xs = Intersections(Intersection(-1, shape), Intersection(1, shape))
        comps = xs[1].prepare_computations(r, xs)
        reflectance = comps.schlick()
        assert reflectance == pytest.approx(0.04)

    def test_schlick_approximation_with_small_angle_and_n2_greater_than_n1(self, glass_sphere):
        shape = glass_sphere()
        r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
        xs = Intersections(Intersection(1.8589, shape))
        comps = xs[0].prepare_computations(r, xs)
        reflectance = comps.schlick()
        assert reflectance == pytest.approx(0.48873, EPSILON)

    @pytest.mark.parametrize("origin,direction,t1,t2", [(Point(5, 0.5, 0), Vector(-1, 0, 0), 4, 6),
                                                        (Point(-5, 0.5, 0), Vector(1, 0, 0), 4, 6),
                                                        (Point(0.5, 5, 0), Vector(0, -1, 0), 4, 6),
                                                        (Point(0.5, -5, 0), Vector(0, 1, 0), 4, 6),
                                                        (Point(0.5, 0, 5), Vector(0, 0, -1), 4, 6),
                                                        (Point(0.5, 0, -5), Vector(0, 0, 1), 4, 6),
                                                        (Point(0, 0.5, 0), Vector(0, 0, 1), -1, 1)])
    def test_ray_intersects_cube(self, origin, direction, t1, t2):
        c = Cube()
        r = Ray(origin, direction)
        xs = c._local_intersect(r)
        assert xs.count == 2
        assert xs[0].t == t1
        assert xs[1].t == t2

    @pytest.mark.parametrize("origin,direction", [(Point(-2, 0, 0), Vector(0.2673, 0.5345, 0.8018)),
                                                  (Point(0, -2, 0), Vector(0.8018, 0.2673, 0.5345)),
                                                  (Point(0, 0, -2), Vector(0.5345, 0.8018, 0.2673)),
                                                  (Point(2, 0, 2), Vector(0, 0, -1)),
                                                  (Point(0, 2, 2), Vector(0, -1, 0)),
                                                  (Point(2, 2, 0), Vector(-1, 0, 0))])
    def test_ray_misses_cube(self, origin, direction):
        c = Cube()
        r = Ray(origin, direction)
        xs = c._local_intersect(r)
        assert xs.count == 0

    def test_intersection_can_encapsulate_u_and_v(self):
        s = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        i = Intersection(3.5, s, 0.2, 0.4)
        assert i.u == 0.2
        assert i.v == 0.4
