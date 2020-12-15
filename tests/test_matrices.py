from raytracer.matrices import Matrix
from raytracer.tuples import Tuple


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
        assert m[0, 2] == 0
        assert m[1, 2] == -7

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

    def test_transpose_matrix(self):
        a = Matrix([[0, 9, 3, 0],
                    [9, 8, 0, 8],
                    [1, 8, 5, 3],
                    [0, 0, 5, 8]])
        assert a.transpose() == Matrix([[0, 9, 1, 0],
                                        [9, 8, 8, 0],
                                        [3, 0, 5, 5],
                                        [0, 8, 3, 8]])

    def test_transpose_identity_matrix(self):
        a = Matrix.identity.transpose()
        assert a == Matrix.identity

    def test_determinant_2x2_matrix(self):
        a = Matrix([[1, 5],
                    [-3, 2]])
        assert a.determinant() == 17

    def test_submatrix_of_3x3_is_2x2(self):
        a = Matrix([[1, 5, 0],
                    [-3, 2, 7],
                    [0, 6, -3]])
        assert a.submatrix(0, 2) == Matrix([[-3, 2],
                                            [0, 6]])

    def test_submatrix_of_4x4_is_3x3(self):
        a = Matrix([[-6, 1, 1, 6],
                    [-8, 5, 8, 6],
                    [-1, 0, 8, 2],
                    [-7, 1, -1, 1]])
        assert a.submatrix(2, 1) == Matrix([[-6, 1, 6],
                                            [-8, 8, 6],
                                            [-7, -1, 1]])

    def test_minor_of_3x3(self):
        a = Matrix([[3, 5, 0],
                    [2, -1, -7],
                    [6, -1, 5]])
        b = a.submatrix(1, 0)
        assert b.determinant() == 25
        assert a.minor(1, 0) == 25

    def test_cofactor_of_3x3(self):
        a = Matrix([[3, 5, 0],
                    [2, -1, -7],
                    [6, -1, 5]])
        assert a.minor(0, 0) == -12
        assert a.cofactor(0, 0) == -12
        assert a.minor(1, 0) == 25
        assert a.cofactor(1, 0) == -25

    def test_determinant_of_3x3(self):
        a = Matrix([[1, 2, 6],
                    [-5, 8, -4],
                    [2, 6, 4]])
        assert a.cofactor(0, 0) == 56
        assert a.cofactor(0, 1) == 12
        assert a.cofactor(0, 2) == -46
        assert a.determinant() == -196

    def test_determinant_of_4x4(self):
        a = Matrix([[-2, -8, 3, 5],
                    [-3, 1, 7, 3],
                    [1, 2, -9, 6],
                    [-6, 7, 7, -9]])
        assert a.cofactor(0, 0) == 690
        assert a.cofactor(0, 1) == 447
        assert a.cofactor(0, 2) == 210
        assert a.cofactor(0, 3) == 51
        assert a.determinant() == -4071

    def test_invertible_matrix_for_invertibility(self):
        a = Matrix([[6, 4, 4, 4],
                    [5, 5, 7, 6],
                    [4, -9, 3, -7],
                    [9, 1, 7, -6]])
        assert a.determinant() == -2120
        assert a.invertible is True

    def test_noninvertible_matrix_for_invertibility(self):
        a = Matrix([[-4, 2, -2, 3],
                    [9, 6, 2, 6],
                    [0, -5, 1, -5],
                    [0, 0, 0, 0]])
        assert a.determinant() == 0
        assert a.invertible is False

    def test_inverse(self):
        a = Matrix([[-5, 2, 6, -8],
                    [1, -5, 1, 8],
                    [7, 7, -6, -7],
                    [1, -3, 7, 4]])
        b = a.inverse()
        assert a.determinant() == 532
        assert a.cofactor(2, 3) == -160
        assert b[3, 2] == -160 / 532
        assert a.cofactor(3, 2) == 105
        assert b[2, 3] == 105 / 532
        assert b == Matrix([[0.21805, 0.45113, 0.24060, -0.04511],
                            [-0.80827, -1.45677, -0.44361, 0.52068],
                            [-0.07895, -0.22368, -0.05263, 0.19737],
                            [-0.52256, -0.81391, -0.30075, 0.30639]])

    def test_inverse2(self):
        a = Matrix([[8, -5, 9, 2],
                    [7, 5, 6, 1],
                    [-6, 0, 9, 6],
                    [-3, 0, -9, -4]])
        assert a.inverse() == Matrix([[-0.15385, -0.15385, -0.28205, -0.53846],
                                      [-0.07692, 0.12308, 0.02564, 0.03077],
                                      [0.35897, 0.35897, 0.43590, 0.92308],
                                      [-0.69231, -0.69231, -0.76923, -1.92308]])

    def test_inverse3(self):
        a = Matrix([[9, 3, 0, 9],
                    [-5, -2, -6, -3],
                    [-4, 9, 6, 4],
                    [-7, 6, 6, 2]])
        assert a.inverse() == Matrix([[-0.04074, -0.07778, 0.14444, -0.22222],
                                      [-0.07778, 0.03333, 0.36667, -0.33333],
                                      [-0.02901, -0.14630, -0.10926, 0.12963],
                                      [0.17778, 0.06667, -0.26667, 0.33333]])

    def test_multiply_product_by_its_inverse(self):
        a = Matrix([[3, -9, 7, 3],
                    [3, -8, 2, -9],
                    [-4, 4, 4, 1],
                    [-6, 5, -1, 1]])
        b = Matrix([[8, 2, 2, 2],
                    [3, -1, 7, 0],
                    [7, 0, 5, 4],
                    [6, -2, 0, 5]])
        c = a * b
        assert c * b.inverse() == a

