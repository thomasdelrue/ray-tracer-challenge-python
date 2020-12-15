from raytracer.tuples import Color
from raytracer.canvas import Canvas


class TestCanvas:
    def test_create_canvas(self):
        c = Canvas(10, 20)
        assert c.width == 10
        assert c.height == 20
        assert c._pixels == [[Color(0, 0, 0) for _ in range(c.height)] for _ in range(c.width)]

    def test_write_pixel_to_canvas(self):
        c = Canvas(10, 20)
        red = Color(1, 0, 0)
        c.write_pixel(2, 3, red)
        assert c.pixel_at(2, 3) == red

    def test_constructing_ppm_header(self):
        c = Canvas(5, 3)
        ppm = c.to_ppm()
        assert ''.join(ppm[:3]) == "P3\n" \
                                   "5 3\n" \
                                   "255\n"

    def test_constructing_ppm_pixel_data(self):
        c = Canvas(5, 3)
        c1 = Color(1.5, 0, 0)
        c2 = Color(0, 0.5, 0)
        c3 = Color(-0.5, 0, 1)
        c.write_pixel(0, 0, c1)
        c.write_pixel(2, 1, c2)
        c.write_pixel(4, 2, c3)
        ppm = c.to_ppm()
        assert ''.join(ppm[3:]) == "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n" \
                                   "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0\n" \
                                   "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255\n"

    def test_splitting_long_lines_in_ppm(self):
        c = Canvas(10, 2)
        for x in range(c.width):
            for y in range(c.height):
                c.write_pixel(x, y, Color(1, 0.8, 0.6))
        ppm = c.to_ppm()
        assert ''.join(ppm[3:]) == "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n"\
                                   "153 255 204 153 255 204 153 255 204 153 255 204 153\n" \
                                   "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n"\
                                   "153 255 204 153 255 204 153 255 204 153 255 204 153\n"

    def test_ppm_files_terminated_with_newline(self):
        c = Canvas(5, 3)
        ppm = c.to_ppm()
        assert ppm[-1][-1] == '\n'
