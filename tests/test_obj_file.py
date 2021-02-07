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

    def test_parsing_triangle_faces(self):
        parser = parse_obj_file(TEST_PATH + 'triangle_faces.obj')
        g = parser.default_group
        t1 = g[0]
        t2 = g[1]
        assert t1.p1 == parser.vertices[1]
        assert t1.p2 == parser.vertices[2]
        assert t1.p3 == parser.vertices[3]
        assert t2.p1 == parser.vertices[1]
        assert t2.p2 == parser.vertices[3]
        assert t2.p3 == parser.vertices[4]

    def test_triangulating_polygons(self):
        parser = parse_obj_file(TEST_PATH + 'triangulating_polygons.obj')
        g = parser.default_group
        t1 = g[0]
        t2 = g[1]
        t3 = g[2]
        assert t1.p1 == parser.vertices[1]
        assert t1.p2 == parser.vertices[2]
        assert t1.p3 == parser.vertices[3]
        assert t2.p1 == parser.vertices[1]
        assert t2.p2 == parser.vertices[3]
        assert t2.p3 == parser.vertices[4]
        assert t3.p1 == parser.vertices[1]
        assert t3.p2 == parser.vertices[4]
        assert t3.p3 == parser.vertices[5]


