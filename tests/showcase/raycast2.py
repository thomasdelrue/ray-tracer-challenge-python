from os import sep
from raytracer.canvas import Canvas, write_ppm_to_file
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.rays import Ray
from raytracer.shapes import Sphere
from raytracer.tuples import Point, Color


if __name__ == '__main__':
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    red = Color(1, 0, 0)
    sphere = Sphere()
    m = Material()
    m.color = Color(1, 0.2, 1)
    sphere.material = m

    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

    for y in range(canvas_pixels):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x

            position = Point(world_x, world_y, wall_z)
            ray = Ray(ray_origin, (position - ray_origin).normalize())
            hit = sphere.intersect(ray).hit()
            if hit:
                point = ray.position(hit.t)
                normal = hit.object.normal_at(point)
                eye = -ray.direction

                color = hit.object.material.lighting(light, point, eye, normal)

                canvas.write_pixel(x, y, color)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}circle.ppm')
