from .canvas import Canvas
from .matrices import Matrix
from .rays import Ray
from .scene import World
from .tuples import Point
import math


class Camera:
    def __init__(self, hsize: int, vsize: int, field_of_view: float):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transformation = Matrix.identity()
        self._derive_properties()

    def _derive_properties(self):
        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        self.pixel_size = (self.half_width * 2) / self.hsize

    def ray_for_pixel(self, px: int, py: int) -> Ray:
        # the offset from the edge of the canvas to the pixel's center
        x_offset = (px + 0.5) * self.pixel_size
        y_offset = (py + 0.5) * self.pixel_size

        # the untransformed coordinates of the pixel in world space.
        # (remember that the camera looks toward -z, so +x is to the *left*.)
        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        # using the camera Matrix, transform the canvas point and the origin,
        # and then compute the ray's direction vector.
        # (remember that canvas is at z=-1)
        pixel = self.transformation.inverse() * Point(world_x, world_y, -1)
        origin = self.transformation.inverse() * Point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)

    def render(self, world: World) -> Canvas:
        image = Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)
            print(f'{int(y / self.vsize * 100)}%')
        return image
