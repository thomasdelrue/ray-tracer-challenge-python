from .shapes import Group, Triangle
from .tuples import Point
from enum import Enum
from typing import List, Callable
import re


vertex_regex = re.compile(r"v (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?)")
faces_regex = re.compile(r"f( \d+){3,}")


class Parser:
    def __init__(self):
        self.ignored_lines = 0
        self.vertices = OneBasedList()
        self.default_group = Group()


class OneBasedList:
    def __init__(self):
        self._collection = []

    def __getitem__(self, index):
        return self._collection[index - 1]

    def append(self, item):
        self._collection.append(item)


def parse_obj_file(obj_file) -> Parser:
    parser = Parser()
    with open(obj_file) as obj:
        for line in obj.readlines():
            _parse_line(line, parser, [_parse_vertices,
                                       _parse_faces])
    return parser


class ParseStatus(Enum):
    PARSED = True
    NOT_PARSED = False


def _parse_line(line: str, parser: Parser, _parse_calls: List[Callable] = []):
    for call in _parse_calls:
        if call(line, parser) == ParseStatus.PARSED:
            return
    parser.ignored_lines += 1


def _parse_vertices(line: str, parser: Parser) -> ParseStatus:
    match = vertex_regex.match(line)
    if match:
        parser.vertices.append(Point(float(match.group(1)),
                                     float(match.group(2)),
                                     float(match.group(3))))
        return ParseStatus.PARSED
    return ParseStatus.NOT_PARSED


def _parse_faces(line: str, parser: Parser):
    match = faces_regex.match(line)
    if match:
        indices = list(map(int, line[2:].split(' ')))
        for i in range(1, len(indices) - 1):
            triangle = Triangle(parser.vertices[indices[0]],
                                parser.vertices[indices[i]],
                                parser.vertices[indices[i + 1]])
            parser.default_group.add_children(triangle)
        return ParseStatus.PARSED
    return ParseStatus.NOT_PARSED
