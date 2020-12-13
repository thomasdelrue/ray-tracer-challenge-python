from typing import List


class Matrix:
    def __init__(self, values: List[List[float]]):
        shape = [len(row) for row in values]
        if len(shape) not in (2, 3, 4) or len(shape) != shape.count(len(shape)):
            raise ValueError("Matrix is not of the shape 2x2, 3x3, or 4x4")
        self.values = values

    def __getitem__(self, key):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            return TypeError("wrong subscript: not an 2-tuple of int")
        return self.values[key[0]][key[1]]

    def __eq__(self, other):
        return self.values == other.values


