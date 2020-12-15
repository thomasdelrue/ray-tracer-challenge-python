from __future__ import annotations
from tuples import Tuple, dot
from typing import List


class Matrix:
    def __init__(self, values: List[List[float]] = None):
        self.values = values if values is not None else [[0, 0, 0, 0] for _ in range(4)]

    @property
    def shape(self):
        rows = len(self.values)
        cols = max([len(col) for col in self.values])
        return max(rows, cols), max(rows, cols)

    def __getitem__(self, key):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            raise TypeError("wrong subscript: not an 2-tuple of int")
        return self.values[key[0]][key[1]]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            raise TypeError("wrong subscript: not an 2-tuple of int")
        self.values[key[0]][key[1]] = value

    def __eq__(self, other):
        return self.values == other.values

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

    def __str__(self):
        return '[' + '\n '.join([str(row) for row in self.values]) + ']'


Matrix.identity = Matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])



