"""Contains the 2D vector class"""

# Standard modules
from typing import Union


class Vec(tuple):
    """2D vector class"""

    def __new__(cls, x: Union[int, float], y: Union[int, float]):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def xy(self):
        return self

    @property
    def yx(self):
        return Vec(self[1], self[0])

    @property
    def xx(self):
        return Vec(self[0], self[0])

    @property
    def yy(self):
        return Vec(self[1], self[1])

    def __add__(self, other):
        return Vec(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Vec(self[0] - other[0], self[1] - other[1])

    def __mul__(self, factor):
        return Vec(self[0] * factor, self[1] * factor)







