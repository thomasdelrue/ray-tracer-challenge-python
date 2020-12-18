from raytracer.intersections import Intersection
from raytracer.lights import PointLight
from raytracer.matrices import scaling
from raytracer.rays import Ray
from raytracer.scene import World
from raytracer.spheres import Sphere
from raytracer.tuples import Point, Color, Vector
import pytest


class TestScene:
    @pytest.fixture
    def default_world(self):
        w = World()
        w.light = PointLight(Point(-10, 10, -10), Color.white())
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2
        s2 = Sphere()
        s2.transformation = scaling(0.5, 0.5, 0.5)
        w.add(s1, s2)
        return w

    def test_create_world(self):
        w = World()
        assert len(w.objects) == 0
        assert w.light is None

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
        w.light = PointLight(Point(0, 0.25, 0), Color.white())
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        i = Intersection(0.5, shape)
        comps = i.prepare_computations(r)
        c = w.shade_hit(comps)
        assert c == Color(0.90498, 0.90498, 0.90498)

