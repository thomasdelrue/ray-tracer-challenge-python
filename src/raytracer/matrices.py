from __future__ import annotations
from math import cos, sin
from raytracer import EPSILON
from .tuples import Tuple, dot, Point, Vector, cross
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
        return Tuple.create_from(*products)

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

    def copy(self):
        copy_values = [row[:] for row in self.values]
        return Matrix(copy_values)

    @staticmethod
    def identity():
        return Matrix([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

    def translate(self, x, y, z):
        return Matrix([[1, 0, 0, x],
                       [0, 1, 0, y],
                       [0, 0, 1, z],
                       [0, 0, 0, 1]]) * self

    def scale(self, x, y, z):
        return scaling(x, y, z) * self

    def rotate_x(self, radians: float):
        return rotation_x(radians) * self

    def rotate_y(self, radians: float):
        return rotation_y(radians) * self

    def rotate_z(self, radians: float):
        return rotation_z(radians) * self

    def shear(self, x2y, x2z, y2x, y2z, z2x, z2y):
        return shearing(x2y, x2z, y2x, y2z, z2x, z2y) * self

    def __str__(self):
        return '[' + '\n '.join([str(row) for row in self.values]) + ']'

    __repr__ = __str__


def translation(x, y, z) -> Matrix:
    tr = Matrix.identity()
    tr[0, 3] = x
    tr[1, 3] = y
    tr[2, 3] = z
    return tr


def scaling(x, y, z) -> Matrix:
    sc = Matrix.identity()
    sc[0, 0] = x
    sc[1, 1] = y
    sc[2, 2] = z
    return sc


def rotation_x(radians: float) -> Matrix:
    rot = Matrix.identity()
    rot[1, 1] = cos(radians)
    rot[1, 2] = -sin(radians)
    rot[2, 1] = sin(radians)
    rot[2, 2] = cos(radians)
    return rot


def rotation_y(radians: float) -> Matrix:
    rot = Matrix.identity()
    rot[0, 0] = cos(radians)
    rot[0, 2] = sin(radians)
    rot[2, 0] = -sin(radians)
    rot[2, 2] = cos(radians)
    return rot


def rotation_z(radians: float) -> Matrix:
    rot = Matrix.identity()
    rot[0, 0] = cos(radians)
    rot[0, 1] = -sin(radians)
    rot[1, 0] = sin(radians)
    rot[1, 1] = cos(radians)
    return rot


def shearing(x2y, x2z, y2x, y2z, z2x, z2y) -> Matrix:
    rot = Matrix.identity()
    rot[0, 1] = x2y
    rot[0, 2] = x2z
    rot[1, 0] = y2x
    rot[1, 2] = y2z
    rot[2, 0] = z2x
    rot[2, 1] = z2y
    return rot


def view_transform(_from: Point, to: Point, up: Vector) -> Matrix:
    forward = (to - _from).normalize()
    left = cross(forward, up.normalize())
    true_up = cross(left, forward)
    orientation = Matrix([[left.x, left.y, left.z, 0],
                          [true_up.x, true_up.y, true_up.z, 0],
                          [-forward.x, -forward.y, -forward.z, 0],
                          [0, 0, 0, 1]])
    return orientation * translation(-_from.x, -_from.y, -_from.z)

