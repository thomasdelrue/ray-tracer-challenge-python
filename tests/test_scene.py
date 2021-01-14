from math import pi, sqrt
from raytracer.camera import Camera
from raytracer.intersections import Intersection, Intersections
from raytracer.lights import PointLight
from raytracer.matrices import scaling, view_transform, translation
from raytracer.rays import Ray
from raytracer.scene import World
from raytracer.shapes import Sphere, Plane
from raytracer.tuples import Point, Color, Vector
from .test_patterns import test_pattern
import pytest


@pytest.fixture
def default_world():
    w = World()
    w.light_source = PointLight(Point(-10, 10, -10), Color.white())
    s1 = Sphere()
    s1.material.color = Color(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2
    s2 = Sphere()
    s2.transformation = scaling(0.5, 0.5, 0.5)
    w.add(s1, s2)
    return w


class TestScene:
    def test_create_world(self):
        w = World()
        assert len(w.objects) == 0
        assert w.light_source is None

    def test_intersect_world_with_ray(self, default_world):
        w = default_world
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = w.intersect(r)
        assert xs.count == 4
        assert xs[0].t == 4
        assert xs[1].t == 4.5
        assert xs[2].t == 5.5
        assert xs[3].t == 6

    def test_shading_intersection(self, default_world):
        w = default_world
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = w.objects[0]
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        assert c == Color(0.38066, 0.47583, 0.2855)

    def test_shading_intersection_from_inside(self, default_world):
        w = default_world
        w.light_source = PointLight(Point(0, 0.25, 0), Color.white())
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        i = Intersection(0.5, shape)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        assert c == Color(0.90498, 0.90498, 0.90498)

    def test_color_black_when_ray_misses(self, default_world):
        w = default_world
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        c = w.color_at(r)
        assert c == Color.black()

    def test_color_when_ray_hits(self, default_world):
        w = default_world
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        c = w.color_at(r)
        assert c == Color(0.38066, 0.47583, 0.2855)

    def test_color_with_intersection_behind_ray(self, default_world):
        w = default_world
        outer = w.objects[0]
        outer.material.ambient = 1
        inner = w.objects[1]
        inner.material.ambient = 1
        r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
        c = w.color_at(r)
        assert c == inner.material.color

    def test_render_world_with_camera(self, default_world):
        w = default_world
        c = Camera(11, 11, pi / 2)
        _from = Point(0, 0, -5)
        to = Point(0, 0, 0)
        up = Vector(0, 2, 0)
        c.transformation = view_transform(_from, to, up)
        image = c.render(w)
        assert image.pixel_at(5, 5) == Color(0.38066, 0.47583, 0.2855)

    def test_no_shadow_when_nothing_collinear_with_point_and_light(self, default_world):
        w = default_world
        p = Point(0, 10, 0)
        assert not w.is_shadowed(p)

    def test_shadow_when_object_is_between_point_and_light(self, default_world):
        w = default_world
        p = Point(10, -10, 10)
        assert w.is_shadowed(p)

    def test_no_shadow_when_object_is_behind_light(self, default_world):
        w = default_world
        p = Point(-20, 20, -20)
        assert not w.is_shadowed(p)

    def test_no_shadow_when_object_is_behind_point(self, default_world):
        w = default_world
        p = Point(-2, 2, -2)
        assert not w.is_shadowed(p)

    def test_shade_hit_is_given_an_intersection_in_shadow(self):
        w = World()
        w.light_source = PointLight(Point(0, 0, -10), Color.white())
        s1 = Sphere()
        s2 = Sphere()
        s2.transformation = translation(0, 0, 10)
        w.add(s1, s2)
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        i = Intersection(4, s2)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        assert c == Color(0.1, 0.1, 0.1)

    def test_reflected_color_for_nonreflective_material(self, default_world):
        w = default_world
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        shape.material.ambient = 1
        i = Intersection(1, shape)
        comps = i.prepare_computations(r)
        color = w.reflected_color(comps)
        assert color == Color.black()

    def test_reflected_color_for_reflective_material(self, default_world):
        w = default_world
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transformation = translation(0, -1, 0)
        w.add(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        i = Intersection(sqrt(2), shape)
        comps = i.prepare_computations(r)
        color = w.reflected_color(comps)
        assert color == Color(0.19033, 0.23791, 0.14274)

    def test_shade_hit_with_reflective_material(self, default_world):
        w = default_world
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transformation = translation(0, -1, 0)
        w.add(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        i = Intersection(sqrt(2), shape)
        comps = i.prepare_computations(r)
        color = w.shade_hit(comps)
        assert color == Color(0.87676, 0.92434, 0.82917)

    def test_color_at_with_mutually_reflective_surfaces(self):
        w = World()
        w.light_source = PointLight(Point(0, 0, 0), Color.white())
        lower = Plane()
        lower.material.reflective = 1
        lower.transformation = translation(0, -1, 0)
        upper = Plane()
        upper.material.reflective = 1
        upper.transformation = translation(0, 1, 0)
        w.add(lower, upper)
        r = Ray(Point(0, 0, 0), Vector(0, 1, 0))

        # Avoid Infinite Recursion
        w.color_at(r)
        assert True

    def test_reflected_color_at_max_recursive_depth(self, default_world):
        w = default_world
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transformation = translation(0, -1, 0)
        w.add(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -sqrt(2) / 2, sqrt(2) / 2))
        i = Intersection(sqrt(2), shape)
        comps = i.prepare_computations(r)
        color = w.reflected_color(comps, 0)
        assert color == Color.black()

    def test_refracted_color_with_opaque_surface(self, default_world):
        w = default_world
        shape = w.objects[0]
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = Intersections(Intersection(4, shape), Intersection(6, shape))
        comps = xs[0].prepare_computations(r, xs)
        c = w.refracted_color(comps, 5)
        assert c == Color.black()

    def test_refracted_color_at_max_recursive_depth(self, default_world):
        w = default_world
        shape = w.objects[0]
        shape.material.transparency = 1.0
        shape.material.refractive_index = 1.5
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = Intersections(Intersection(4, shape), Intersection(6, shape))
        comps = xs[0].prepare_computations(r, xs)
        c = w.refracted_color(comps, 0)
        assert c == Color.black()

    def test_refracted_color_under_total_internal_reflection(self, default_world):
        w = default_world
        shape = w.objects[0]
        shape.material.transparency = 1.0
        shape.material.refractive_index = 1.5
        r = Ray(Point(0, 0, sqrt(2) / 2), Vector(0, 1, 0))
        xs = Intersections(Intersection(-sqrt(2) / 2, shape), Intersection(sqrt(2) / 2, shape))
        # NOTE: this time you're inside the sphere, so you need
        # to look at the second intersection, xs[1], not xs[0]
        comps = xs[1].prepare_computations(r, xs)
        c = w.refracted_color(comps, 5)
        assert c == Color.black()

    def test_refracted_color_with_refracted_ray(self, default_world):
        w = default_world
        a = w.objects[0]
        a.material.ambient = 1.0
        a.material.pattern = test_pattern()
        b = w.objects[1]
        b.material.transparency = 1.0
        b.material.refractive_index = 1.5
        r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
        xs = Intersections(Intersection(-0.9899, a), Intersection(-0.4899, b),
                           Intersection(0.4899, b), Intersection(0.9899, a))
        comps = xs[2].prepare_computations(r, xs)
        c = w.refracted_color(comps, 5)
        assert c == Color(0, 0.99888, 0.04722)

