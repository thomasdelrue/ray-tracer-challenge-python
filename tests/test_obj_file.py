from os import sep
from raytracer.obj_file import parse_obj_file
from raytracer.tuples import Point, Vector


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
        g = parser.active_group
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
        g = parser.active_group
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

    def test_triangles_in_groups(self):
        parser = parse_obj_file(TEST_PATH + 'triangle_groups.obj')
        g1 = parser['FirstGroup']
        g2 = parser['SecondGroup']
        t1 = g1[0]
        t2 = g2[0]
        assert t1.p1 == parser.vertices[1]
        assert t1.p2 == parser.vertices[2]
        assert t1.p3 == parser.vertices[3]
        assert t2.p1 == parser.vertices[1]
        assert t2.p2 == parser.vertices[3]
        assert t2.p3 == parser.vertices[4]

    def test_converting_obj_file_to_group(self):
        parser = parse_obj_file(TEST_PATH + 'triangle_groups.obj')
        g = parser.obj_to_group()

        group_names = list(map(lambda x: x.name, g))
        assert 'FirstGroup' in group_names
        assert 'SecondGroup' in group_names

    def test_vertex_normal_records(self):
        parser = parse_obj_file(TEST_PATH + 'vertex_normals.obj')
        assert parser.normals[1] == Vector(0, 0, 1)
        assert parser.normals[2] == Vector(0.707, 0, -0.707)
        assert parser.normals[3] == Vector(1, 2, 3)

    def test_faces_with_normals(self):
        parser = parse_obj_file(TEST_PATH + 'triangle_faces_with_normals.obj')
        g = parser['default']
        t1 = g[0]
        t2 = g[1]
        assert t1.p1 == parser.vertices[1]
        assert t1.p2 == parser.vertices[2]
        assert t1.p3 == parser.vertices[3]
        assert t1.n1 == parser.normals[3]
        assert t1.n2 == parser.normals[1]
        assert t1.n3 == parser.normals[2]
        assert (t1.p1, t1.p2, t1.p3, t1.n1, t1.n2, t1.n3) == \
               (t2.p1, t2.p2, t2.p3, t2.n1, t2.n2, t2.n3)
