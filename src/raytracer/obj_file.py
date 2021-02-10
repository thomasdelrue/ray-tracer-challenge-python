from .shapes import Group, Triangle, SmoothTriangle
from .tuples import Point, Vector
from enum import Enum
from typing import List, Callable
import re
import time


vertex_regex = re.compile(r"v (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?)")
vertex_normal_regex = re.compile(r"vn (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?)")
faces_regex = re.compile(r"f( (?P<v>\d+)(/\d*/(?P<vn>\d*))?){3,}")
face_el_regex = re.compile(r"(?P<v>\d+)(/\d*/(?P<vn>\d+))?")
group_regex = re.compile(r"g (\w+)")


class Parser:
    def __init__(self):
        self.ignored_lines = 0
        self.vertices = OneBasedList()
        self.normals = OneBasedList()
        self._groups = {'default': Group()}
        self._active_group = 'default'

    @property
    def active_group(self) -> Group:
        return self._groups[self._active_group]

    @active_group.setter
    def active_group(self, current: str):
        if current not in self._groups:
            self._groups[current] = Group(current)
        self._active_group = current

    def __getitem__(self, group):
        return self._groups[group]

    def obj_to_group(self) -> Group:
        group = Group("obj")
        for subgroup in self._groups.values():
            group.add_children(subgroup)
        return group


class OneBasedList:
    def __init__(self):
        self._collection = []

    def __getitem__(self, index):
        return self._collection[index - 1]

    def append(self, item):
        self._collection.append(item)


def parse_obj_file(obj_file) -> Parser:
    parser = Parser()

    print(f'Parsing...')
    start = time.perf_counter()
    with open(obj_file) as obj:
        for i, line in enumerate(obj.readlines()):
            _parse_line(line, parser, [_parse_vertices,
                                       _parse_vertex_normals,
                                       _parse_faces,
                                       _parse_groups])
    duration = time.perf_counter() - start
    print(f'Parsed in {duration:.2f} seconds')
    return parser


class ParseStatus(Enum):
    PARSED = True
    NOT_PARSED = False


def _parse_line(line: str, parser: Parser, _parse_calls: List[Callable]):
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


def _parse_vertex_normals(line: str, parser: Parser) -> ParseStatus:
    match = vertex_normal_regex.match(line)
    if match:
        parser.normals.append(Vector(float(match.group(1)),
                                     float(match.group(2)),
                                     float(match.group(3))))
        return ParseStatus.PARSED
    return ParseStatus.NOT_PARSED


def _parse_faces(line: str, parser: Parser):
    match = faces_regex.match(line)
    if match:
        elements = line[2:].split(' ')
        v_indices, vn_indices = [], []
        for el in elements:
            matches = face_el_regex.match(el).groupdict()
            v_indices.append(int(matches['v']))
            if matches['vn']:
                vn_indices.append(int(matches['vn']))

        if len(v_indices) != len(vn_indices):
            for i in range(1, len(v_indices) - 1):
                triangle = Triangle(parser.vertices[v_indices[0]],
                                    parser.vertices[v_indices[i]],
                                    parser.vertices[v_indices[i + 1]])
                parser.active_group.add_children(triangle)

        else:
            for i in range(1, len(v_indices) - 1):
                triangle = SmoothTriangle(parser.vertices[v_indices[0]],
                                          parser.vertices[v_indices[i]],
                                          parser.vertices[v_indices[i + 1]],
                                          parser.normals[vn_indices[0]],
                                          parser.normals[vn_indices[i]],
                                          parser.normals[vn_indices[i + 1]])
                parser.active_group.add_children(triangle)

        return ParseStatus.PARSED
    return ParseStatus.NOT_PARSED


def _parse_groups(line: str, parser: Parser):
    match = group_regex.match(line)
    if match:
        parser.active_group = match.group(1)
        return ParseStatus.PARSED
    return ParseStatus.NOT_PARSED
