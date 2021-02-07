from os import sep
from raytracer.obj_file import parse_obj_file
from raytracer.tuples import Point


TEST_PATH = f'tests{sep}resources{sep}'


class TestObjFile:
    def test_ignoring_unrecognised_lines(self):
        parser = parse_obj_file(TEST_PATH + 'gibberish.obj')
        assert parser.ignored_lines == 5

    def test_vertex_records(self):
        parser = parse_obj_file(TEST_PATH + 'vertex_records.obj')
        assert parser.vertices[1] == Point(-1, 1, 0)
        assert parser.vertices[2] == Point(-1, 0.5, 0)
        assert parser.vertices[3] == Point(1, 0, 0)
        assert parser.vertices[4] == Point(1, 1, 0)


