"""Contains the 2D vector class"""

# Standard modules
from typing import Union, Self
import math


class Vec(tuple):
    """2D vector class"""

    def __new__(cls, x: Union[int, float], y: Union[int, float]) -> Self:
        return tuple.__new__(cls, (x, y))

    @property
    def x(self) -> Union[int, float]:
        return self[0]

    @property
    def y(self) -> Union[int, float]:
        return self[1]

    @property
    def xy(self) -> Self:
        return self

    @property
    def yx(self) -> Self:
        return Vec(self[1], self[0])

    @property
    def xx(self) -> Self:
        return Vec(self[0], self[0])

    @property
    def yy(self) -> Self:
        return Vec(self[1], self[1])

    @property
    def rounded(self) -> bool:
        return isinstance(self[0], int) and isinstance(self[1], int)

    @property
    def normalized(self) -> bool:
        return self.length == 1

    @property
    def length(self) -> float:
        return math.sqrt(self[0] ** 2 + self[1] ** 2)

    @property
    def length_squared(self) -> float:
        return self[0] ** 2 + self[1] ** 2

    def list(self) -> list[Union[int, float]]:
        """Create a list with the x and y values as elements"""
        return [*self]

    def dict(self, keys: tuple[str, str] = ("x", "y")) -> dict[str, Union[int, float]]:
        """Create a dictionary with the x and y values as value of specific keys"""
        return {keys[0]: self[0], keys[1]: self[1]}

    def distance(self, other: Self) -> float:
        """Calculate the distance to another vector"""
        return math.sqrt(pow(self[0] - other[0], 2) + pow(self[1] - other[1], 2))

    def distance_squared(self, other: Self) -> float:
        """Calculate the squared distance to another vector"""
        return abs(self[0] - other[0]) + abs(self[1] - other[1])

    def normalize(self) -> Self:
        """Normalize the vector to a length of 1"""
        if self.length == 0:
            return Vec(0, 0)
        return self.__truediv__(self.length)

    def round(self, n: int = None) -> Self:
        """Round the vector to a vector with integer values"""
        return self.__round__(n)

    def floor(self) -> Self:
        """Floor the vector to a vector with integer values"""
        return self.__floor__()

    def ceil(self) -> Self:
        """Ceil the vector to a vector with integer values"""
        return self.__ceil__()

    def __eq__(self, other: Self) -> bool:
        return self[0] == other[0] and self[1] == other[1]

    def __ne__(self, other: Self) -> bool:
        return self[0] != other[0] or self[1] != other[1]

    def __add__(self, other: Self) -> Self:
        return Vec(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other: Self) -> Self:
        return Vec(self[0] - other[0], self[1] - other[1])

    def __mul__(self, factor: Union[int, float]) -> Self:
        return Vec(self[0] * factor, self[1] * factor)

    def __truediv__(self, divisor: Union[int, float]) -> Self:
        return Vec(self[0] / divisor, self[1] / divisor)

    def __floordiv__(self, divisor: Union[int, float]) -> Self:
        return Vec(self[0] // divisor, self[1] // divisor)

    def __pow__(self, power: float, modulo: float = None):
        return Vec(pow(self[0], power, modulo), pow(self[1], power, modulo))

    def __round__(self, n: int = None) -> Self:
        return Vec(round(self[0], n), round(self[1], n))

    def __floor__(self) -> Self:
        return Vec(math.floor(self[0]), math.floor(self[1]))

    def __ceil__(self) -> Self:
        return Vec(math.ceil(self[0]), math.ceil(self[1]))

    def __abs__(self) -> Self:
        return Vec(abs(self[0]), abs(self[1]))

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return Vec(-self[0], -self[1])

    def __repr__(self) -> str:
        return f"Vec[id={id(self)}, x={self[0]}, y={self[1]}]"

    def __str__(self) -> str:
        return f"({self[0]}, {self[1]})"
