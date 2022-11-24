"""Contains the 3D vector class"""

# Standard modules
from typing import Union, Self
import math

# Local modules
from .vector2d import Vec


class Vec3(tuple):
    """3D vector class"""

    def __new__(cls, x: Union[int, float], y: Union[int, float], z: Union[int, float]) -> Self:
        return tuple.__new__(cls, (x, y, z))

    @property
    def x(self) -> Union[int, float]:
        return self[0]

    @property
    def y(self) -> Union[int, float]:
        return self[1]

    @property
    def z(self) -> Union[int, float]:
        return self[2]

    @property
    def xx(self) -> Vec:
        return Vec(self[0], self[0])

    @property
    def yy(self) -> Vec:
        return Vec(self[1], self[1])

    @property
    def zz(self) -> Vec:
        return Vec(self[2], self[2])

    @property
    def xy(self) -> Vec:
        return Vec(self[0], self[1])

    @property
    def xz(self) -> Vec:
        return Vec(self[0], self[2])

    @property
    def yx(self) -> Vec:
        return Vec(self[1], self[0])

    @property
    def yz(self) -> Vec:
        return Vec(self[1], self[2])

    @property
    def zx(self) -> Vec:
        return Vec(self[2], self[0])

    @property
    def zy(self) -> Vec:
        return Vec(self[2], self[1])

    @property
    def xxx(self) -> Self:
        return Vec3(self[0], self[0], self[0])

    @property
    def xyy(self) -> Self:
        return Vec3(self[0], self[1], self[1])

    @property
    def xzz(self) -> Self:
        return Vec3(self[0], self[2], self[2])

    @property
    def xxy(self) -> Self:
        return Vec3(self[0], self[0], self[1])

    @property
    def xxz(self) -> Self:
        return Vec3(self[0], self[0], self[2])

    @property
    def xyx(self) -> Self:
        return Vec3(self[0], self[1], self[0])

    @property
    def xyz(self) -> Self:
        return self

    @property
    def xzx(self) -> Self:
        return Vec3(self[0], self[2], self[0])

    @property
    def xzy(self) -> Self:
        return Vec3(self[0], self[2], self[1])

    @property
    def yxx(self) -> Self:
        return Vec3(self[1], self[0], self[0])

    @property
    def yyy(self) -> Self:
        return Vec3(self[1], self[1], self[1])

    @property
    def yzz(self) -> Self:
        return Vec3(self[1], self[2], self[2])

    @property
    def yxy(self) -> Self:
        return Vec3(self[1], self[0], self[1])

    @property
    def yxz(self) -> Self:
        return Vec3(self[1], self[0], self[2])

    @property
    def yyx(self) -> Self:
        return Vec3(self[1], self[1], self[0])

    @property
    def yyz(self) -> Self:
        return Vec3(self[1], self[1], self[2])

    @property
    def yzx(self) -> Self:
        return Vec3(self[1], self[2], self[0])

    @property
    def yzy(self) -> Self:
        return Vec3(self[1], self[2], self[1])

    @property
    def zxx(self) -> Self:
        return Vec3(self[2], self[0], self[0])

    @property
    def zyy(self) -> Self:
        return Vec3(self[2], self[1], self[1])

    @property
    def zzz(self) -> Self:
        return Vec3(self[2], self[2], self[2])

    @property
    def zxy(self) -> Self:
        return Vec3(self[2], self[0], self[1])

    @property
    def zxz(self) -> Self:
        return Vec3(self[2], self[0], self[2])

    @property
    def zyx(self) -> Self:
        return Vec3(self[2], self[1], self[0])

    @property
    def zyz(self) -> Self:
        return Vec3(self[2], self[1], self[2])

    @property
    def zzx(self) -> Self:
        return Vec3(self[2], self[2], self[0])

    @property
    def zzy(self) -> Self:
        return Vec3(self[2], self[2], self[1])

    @property
    def rounded(self) -> bool:
        return isinstance(self[0], int) and isinstance(self[1], int) and isinstance(self[2], int)

    @property
    def normalized(self) -> bool:
        return self.length == 1

    @property
    def length(self) -> float:
        return math.sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)

    @property
    def length_squared(self) -> float:
        return self[0] ** 2 + self[1] ** 2 + self[2] ** 2

    def list(self) -> list[Union[int, float]]:
        """Create a list with the x and y values as elements"""
        return [*self]

    def dict(self, keys: tuple[str, str, str] = ("x", "y", "z")) -> dict[str, Union[int, float]]:
        """Create a dictionary with the x and y values as value of specific keys"""
        return {keys[0]: self[0], keys[1]: self[1], keys[2]: self[2]}

    def distance(self, other: Self) -> float:
        """Calculate the distance to another vector"""
        return math.sqrt(pow(self[0] - other[0], 2) + pow(self[1] - other[1], 2) + pow(self[2] - other[2], 2))

    def distance_squared(self, other: Self) -> float:
        """Calculate the squared distance to another vector"""
        return abs(self[0] - other[0]) + abs(self[1] - other[1]) + abs(self[2] - other[2])

    def normalize(self) -> Self:
        """Normalize the vector to a length of 1"""
        if self.length == 0:
            return Vec3(0, 0, 0)
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
        return self[0] == other[0] and self[1] == other[1] and self[2] == other[2]

    def __ne__(self, other: Self) -> bool:
        return self[0] != other[0] or self[1] != other[1] or self[2] != other[2]

    def __add__(self, other: Self) -> Self:
        return Vec3(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other: Self) -> Self:
        return Vec3(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, factor: Union[int, float]) -> Self:
        return Vec3(self[0] * factor, self[1] * factor, self[2] * factor)

    def __truediv__(self, divisor: Union[int, float]) -> Self:
        return Vec3(self[0] / divisor, self[1] / divisor, self[2] / divisor)

    def __floordiv__(self, divisor: Union[int, float]) -> Self:
        return Vec3(self[0] // divisor, self[1] // divisor, self[2] // divisor)

    def __pow__(self, power: float, modulo: float = None):
        return Vec3(pow(self[0], power, modulo), pow(self[1], power, modulo), pow(self[2], power, modulo))

    def __round__(self, n: int = None) -> Self:
        return Vec3(round(self[0], n), round(self[1], n), round(self[2], n))

    def __floor__(self) -> Self:
        return Vec3(math.floor(self[0]), math.floor(self[1]), math.floor(self[2]))

    def __ceil__(self) -> Self:
        return Vec3(math.ceil(self[0]), math.ceil(self[1]), math.ceil(self[2]))

    def __abs__(self) -> Self:
        return Vec3(abs(self[0]), abs(self[1]), abs(self[2]))

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return Vec3(-self[0], -self[1], -self[2])

    def __repr__(self) -> str:
        return f"Vec3[id={id(self)}, x={self[0]}, y={self[1]}, z={self[2]}]"

    def __str__(self) -> str:
        return f"({self[0]}, {self[1]}, {self[2]})"
