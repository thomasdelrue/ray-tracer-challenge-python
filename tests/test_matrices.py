from matrices import Matrix
from tuples import Tuple


class TestMatrices:
    def test_construct_4x4_matrix(self):
        m = Matrix([[1, 2, 3, 4],
                    [5.5, 6.5, 7.5, 8.5],
                    [9, 10, 11, 12],
                    [13.5, 14.5, 15.5, 16.5]])
        assert m[0, 0] == 1
        assert m[0, 3] == 4
        assert m[1, 0] == 5.5
        assert m[1, 2] == 7.5
        assert m[2, 2] == 11
        assert m[3, 0] == 13.5
        assert m[3, 2] == 15.5

    def test_construct_2x2_matrix(self):
        m = Matrix([[-3, 5],
                    [1, -2]])
        assert m[0, 0] == -3
        assert m[0, 1] == 5
        assert m[1, 0] == 1
        assert m[1, 1] == -2

    def test_construct_3x3_matrix(self):
        m = Matrix([[-3, 5, 0],
                    [1, -2, -7],
                    [0, 1, 1]])

    def test_matrix_equality_with_identical_matrices(self):
        a = Matrix([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 8, 7, 6],
                    [5, 4, 3, 2]])
        b = Matrix([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 8, 7, 6],
                    [5, 4, 3, 2]])
        assert a == b

    def test_matrix_equality_with_different_matrices(self):
        a = Matrix([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 8, 7, 6],
                    [5, 4, 3, 2]])
        b = Matrix([[2, 3, 4, 5],
                    [6, 7, 8, 9],
                    [8, 7, 6, 5],
                    [4, 3, 2, 1]])
        assert a != b

    def test_multiply_two_matrices(self):
        a = Matrix([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 8, 7, 6],
                    [5, 4, 3, 2]])
        b = Matrix([[-2, 1, 2, 3],
                    [3, 2, 1, -1],
                    [4, 3, 6, 5],
                    [1, 2, 7, 8]])
        assert a * b == Matrix([[20, 22, 50, 48],
                                [44, 54, 114, 108],
                                [40, 58, 110, 102],
                                [16, 26, 46, 42]])

    def test_matrix_multiplied_by_tuple(self):
        a = Matrix([[1, 2, 3, 4],
                    [2, 4, 4, 2],
                    [8, 6, 4, 1],
                    [0, 0, 0, 1]])
        b = Tuple(1, 2, 3, 1)
        assert a * b == Tuple(18, 24, 33, 1)

    def test_multiply_matrix_by_identity_matric(self):
        a = Matrix([[0, 1, 2, 4],
                    [1, 2, 4, 8],
                    [2, 4, 8, 16],
                    [4, 8, 16, 32]])
        assert a * Matrix.identity == a

    def test_multiply_identity_matrix_by_tuple(self):
        a = Tuple(1, 2, 3, 4)
        assert Matrix.identity * a == a
