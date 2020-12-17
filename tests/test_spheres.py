from math import sqrt, pi
from raytracer.materials import Material
from raytracer.matrices import Matrix, translation, scaling, rotation_z
from raytracer.rays import Ray
from raytracer.spheres import Sphere
from raytracer.tuples import Vector, Point


class TestSpheres:
    def test_ray_intersects_sphere_at_two_points(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].t == 4.0
        assert xs[1].t == 6.0

    def test_ray_intersects_sphere_at_tangent(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].t == 5.0
        assert xs[1].t == 5.0

    def test_ray_misses_sphere(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 0

    def test_ray_originates_inside_sphere(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].t == -1.0
        assert xs[1].t == 1.0

    def test_sphere_is_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].t == -6.0
        assert xs[1].t == -4.0

    def test_intersect_sets_object_on_the_intersection(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].object == s
        assert xs[1].object == s

    def test_sphere_default_transformation(self):
        s = Sphere()
        assert s.transformation == Matrix.identity()

    def test_change_transformation_of_sphere(self):
        s = Sphere()
        t = translation(2, 3, 4)
        s.transformation = t
        assert s.transformation == t

    def test_intersecting_scaled_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transformation = scaling(2, 2, 2)
        xs = s.intersect(r)
        assert xs.count == 2
        assert xs[0].t == 3
        assert xs[1].t == 7

    def test_intersecting_translated_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transformation = translation(5, 0, 0)
        xs = s.intersect(r)
        assert xs.count == 0

    def test_normal_sphere_at_point_on_x_axis(self):
        s = Sphere()
        n = s.normal_at(Point(1, 0, 0))
        assert n == Vector(1, 0, 0)

    def test_normal_sphere_at_point_on_y_axis(self):
        s = Sphere()
        n = s.normal_at(Point(0, 1, 0))
        assert n == Vector(0, 1, 0)

    def test_normal_sphere_at_point_on_z_axis(self):
        s = Sphere()
        n = s.normal_at(Point(0, 0, 1))
        assert n == Vector(0, 0, 1)

    def test_normal_sphere_at_nonaxial_point(self):
        s = Sphere()
        n = s.normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
        assert n == Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)

    def test_normal_is_normalized_vector(self):
        s = Sphere()
        n = s.normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
        assert n == n.normalize()

    def test_compute_normal_on_translated_sphere(self):
        s = Sphere()
        s.transformation = translation(0, 1, 0)
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        assert n == Vector(0, 0.70711, -0.70711)

    def test_compute_normal_on_transformed_sphere(self):
        s = Sphere()
        s.transformation = scaling(1, 0.5, 1) * rotation_z(pi / 5)
        n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))
        assert n == Vector(0, 0.97014, -0.24254)

    def test_sphere_has_default_material(self):
        s = Sphere()
        assert s.material == Material()

    def test_sphere_may_have_material_assigned(self):
        s = Sphere()
        m = Material()
        m.ambient = 1
        s.material = m
        assert s.material == m


