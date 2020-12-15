from os import sep
from canvas import Canvas, write_ppm_to_file
from tuples import Point, Vector, Color
from tests.projectiles import Projectile, Environment, tick


def plot_point_on_canvas(p: Point, c: Canvas):
    x, y = int(p.x), c.height - int(p.y)
    if 0 <= x <= c.width and 0 <= y <= c.height:
        c.write_pixel(x, y, Color(1, 0, 0))


if __name__ == '__main__':
    start = Point(0, 1, 0)
    velocity = Vector(1, 1.8, 0).normalize() * 11.25
    proj = Projectile(start, velocity)

    env = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))

    canvas = Canvas(900, 550)
    while proj.position.y > 0:
        proj = tick(env, proj)
        plot_point_on_canvas(proj.position, canvas)

    write_ppm_to_file(canvas.to_ppm(), f'..{sep}resources{sep}proj2.ppm')
