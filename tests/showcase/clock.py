from os import sep
from raytracer.canvas import Canvas, write_ppm_to_file
from raytracer.tuples import Point, Color
from raytracer.matrices import rotation_z
from typing import List
import math


def plot_points_on_canvas(ps: List[Point], c: Canvas):
    blue = Color(0, 0, 1)
    for p in ps:
        x, y = int(p.x + c.width / 2), int(p.y + c.height / 2)
        print(f'x={x}, y={y}')
        if 0 <= x < c.width and 0 <= y < c.height:
            c.write_pixel(x, y, blue)


if __name__ == '__main__':
    canvas = Canvas(120, 120)
    points = []

    middle = Point(0, 0, 0)
    points.append(middle)

    hour = Point(0, -30, 0)
    points.append(hour)
    for _ in range(1, 12):
        hour = rotation_z(math.pi / 6) * hour
        points.append(hour)

    plot_points_on_canvas(points, canvas)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}..{sep}resources{sep}clock.ppm')
