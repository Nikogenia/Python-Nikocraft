# Standard modules
from typing import List


class EnumError(Exception):
    """A error for invalid usage of enums"""
    pass


class EnumMeta(type):
    """The metaclass for an enum"""

    __unique = 1

    def __new__(mcs, name, bases, attrs):

        # Create class
        attrs["__build__"] = None
        attrs["__type__"] = None
        __enum = type.__new__(mcs, name, bases, attrs)

        # Generate enum elements
        for attr, value in __enum.__annotations__.items():
            if value == int:
                mcs.__define_type(__enum, "int")
                setattr(__enum, attr, mcs.__unique)
                mcs.__unique += 1
            elif value == str:
                mcs.__define_type(__enum, "str")
                setattr(__enum, attr, attr)
        for attr, value in attrs.items():
            if value.__class__ == tuple:
                mcs.__define_type(__enum, "cls")
                setattr(__enum, attr, __enum(*value))
                __enum.__annotations__[attr] = __enum

        # Return class
        delattr(__enum, "__build__")
        return __enum

    def __setattr__(cls, key, value):
        if "__build__" not in cls.__dict__:
            raise EnumError("Changing of enum elements is not allowed!")
        type.__setattr__(cls, key, value)

    def __contains__(cls, item):
        cls.__check_enum(cls)
        return item in getattr(cls, "values") or item in cls.__dict__.keys()

    def __iter__(cls):
        cls.__check_enum(cls)
        return iter(getattr(cls, "values"))

    def __getitem__(cls, item):
        if item not in cls:
            raise KeyError(f"Cannot find '{item}' in '{cls}'!")
        return getattr(cls, item)

    @staticmethod
    def __define_type(enum, name):
        if enum.__dict__["__type__"] not in [None, name]:
            raise EnumError("Invalid enum declaration! Can't use different types together!")
        setattr(enum, "__type__", name)

    @staticmethod
    def __check_enum(enum):
        if not hasattr(enum, "values"):
            raise EnumError("Enums need to inherit from Enum (not EnumMeta)!")

    @property
    def values(cls) -> List:
        """Returns all enum elements as a list"""

        elements = []
        for a, v in cls.__dict__.items():
            if a.startswith("__"):
                continue
            if v.__class__ in [cls, int, str]:
                elements.append(v)
        return elements


class Enum(metaclass=EnumMeta):
    """The enum class

    Integer enum:
    elem1: int
    elem2: int
    ...

    Generates a enum with automatic assignment of a unique number


    String enum:
    elem1: str
    elem2: str
    ...

    Generates a enum with automatic assignment of the element name as string


    Custom enum:
    elem1 = arg1, arg2, ...
    elem2 = arg1, arg2, ...
    ...

    Generates a enum with the tuple values as arguments for the enum objects as elements

    """

    def __get__(self, instance, owner):
        if instance is not None:
            raise EnumError("Accessing enum elements from instance is not allowed!")
        return self
