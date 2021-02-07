from .tuples import Point
import re


vertex_regex = re.compile(r"v (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?) (-?\d*(?:.\d*)?)")


class Parser:
    def __init__(self):
        self.ignored_lines = 0
        self.vertices = OneBasedList()


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
            match = vertex_regex.match(line)
            if match:
                parser.vertices.append(Point(float(match.group(1)),
                                             float(match.group(2)),
                                             float(match.group(3))))
            else:
                parser.ignored_lines += 1
    return parser


