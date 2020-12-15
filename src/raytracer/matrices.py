from __future__ import annotations
from raytracer import EPSILON
from raytracer.tuples import Tuple, dot
from typing import List


class Matrix:
    def __init__(self, values: List[List[float]] = None):
        self.values = values if values is not None else [[0, 0, 0, 0] for _ in range(4)]

    @property
    def size(self):
        rows = len(self.values)
        cols = max([len(col) for col in self.values])
        return max(rows, cols)

    def __getitem__(self, key):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            raise TypeError("wrong subscript: not an 2-tuple of int")
        return self.values[key[0]][key[1]]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            raise TypeError("wrong subscript: not an 2-tuple of int")
        self.values[key[0]][key[1]] = value

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for row in range(self.size):
            for col in range(self.size):
                if abs(self[row, col] - other[row, col]) >= EPSILON:
                    return False
        return True

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self._multiply_by_matrix(other)
        elif isinstance(other, Tuple):
            return self._multiply_by_tuple(other)
        raise TypeError(f"multiplying matrix by {type(other)} not supported")

    def _multiply_by_matrix(self, other: Matrix):
        m = Matrix()
        for row in range(4):
            for col in range(4):
                m[row, col] = self[row, 0] * other[0, col] + \
                              self[row, 1] * other[1, col] + \
                              self[row, 2] * other[2, col] + \
                              self[row, 3] * other[3, col]
        return m

    def _multiply_by_tuple(self, _tuple: Tuple):
        products = []
        for row in range(4):
            result = dot(Tuple(*self.values[row]), _tuple)
            products.append(result)
        return Tuple(*products)

    def row(self, row_nr):
        return self.values[row_nr]

    def col(self, col_nr):
        return [r[col_nr] for r in self.values]

    def transpose(self) -> Matrix:
        m = Matrix()
        size = self.size
        for row in range(size):
            for col in range(size):
                m[row, col] = self[col, row]
        return m

    def determinant(self) -> float:
        if self.size == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        else:
            products = [el * self.cofactor(0, col) for col, el in enumerate(self.values[0])]
            return sum(products)

    def submatrix(self, row, col):
        values = [r[:col] + r[col + 1:] for i, r in enumerate(self.values) if i != row]
        return Matrix(values)

    def minor(self, row, col):
        return self.submatrix(row, col).determinant()

    def cofactor(self, row, col):
        if (row + col) % 2:
            return -self.minor(row, col)
        else:
            return self.minor(row, col)

    @property
    def invertible(self) -> bool:
        return self.determinant() != 0

    def inverse(self):
        if not self.invertible:
            raise ValueError('matrix is invertible')
        inverted = Matrix([[0] * self.size for _ in range(self.size)])
        det = self.determinant()
        for row in range(self.size):
            for col in range(self.size):
                cf = self.cofactor(row, col)
                inverted[col, row] = cf / det
        return inverted

    def __str__(self):
        return '[' + '\n '.join([str(row) for row in self.values]) + ']'

    __repr__ = __str__


Matrix.identity = Matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
