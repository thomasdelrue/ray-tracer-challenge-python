from tuples import Color
from typing import List


class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pixels = [[Color(0, 0, 0) for _ in range(height)] for _ in range(width)]

    def write_pixel(self, x: int, y: int, color: Color) -> None:
        self._pixels[x][y] = color

    def pixel_at(self, x: int, y: int) -> Color:
        return self._pixels[x][y]

    def to_ppm(self):
        max_color_value: int = 255
        ppm_header = ['P3\n', f'{self.width} {self.height}\n', f'{max_color_value}\n']
        pixel_data = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                color = self.pixel_at(x, y)
                pixel = tuple(map(lambda c: min(max(0, round(c * max_color_value)), max_color_value), color))
                for index in range(3):
                    text = f'{pixel[index]} '
                    if len(line + text) <= 70:
                        line += text
                    else:
                        pixel_data.append(line[:-1] + '\n')
                        line = text
            pixel_data.append(line[:-1] + '\n')
        ppm = ppm_header + pixel_data
        return ppm


def write_ppm_to_file(ppm: List[str], file_name: str) -> None:
    with open(file_name, 'wt') as file:
        file.writelines(ppm)
