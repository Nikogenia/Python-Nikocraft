"""Contains the enum class and metaclass"""


class EnumError(Exception):
    """A error for invalid usage of enums"""
    pass


class EnumMeta(type):
    """The metaclass for an enum"""

    __unique = 1

    def __new__(mcs, name, bases, attrs):

        # Create class
        attrs["__build__"] = None
        __enum = type.__new__(mcs, name, bases, attrs)

        # Generate enum elements
        for attr, value in __enum.__annotations__.items():
            if value == int:
                setattr(__enum, attr, mcs.__unique)
                mcs.__unique += 1
            elif value == str:
                setattr(__enum, attr, attr)

        # Return class
        delattr(__enum, "__build__")
        return __enum

    def __setattr__(cls, key, value):
        if "__build__" not in cls.__dict__:
            raise EnumError("Changing enum elements is not allowed!")
        type.__setattr__(cls, key, value)

    def __delattr__(cls, key):
        if "__build__" not in cls.__dict__:
            raise EnumError("Deleting enum elements is not allowed!")
        type.__delattr__(cls, key)

    def __contains__(cls, item):
        cls.__check_enum(cls)
        return item in getattr(cls, "values") or item in cls.__dict__.keys()

    def __iter__(cls):
        cls.__check_enum(cls)
        return iter(getattr(cls, "values"))

    def __len__(cls):
        return len(getattr(cls, "values"))

    def __getitem__(cls, item):
        if item not in cls:
            raise KeyError(f"Cannot find '{item}' in '{cls}'!")
        return getattr(cls, item)

    def __setitem__(cls, item, value):
        raise EnumError("Changing enum elements is not allowed!")

    def __delitem__(cls, item):
        raise EnumError("Deleting enum elements is not allowed!")

    def __call__(cls, element: str):
        if element not in cls:
            raise KeyError(f"Cannot find '{element}' in '{cls}'!")
        return getattr(cls, element)

    @staticmethod
    def __check_enum(enum) -> None:
        if not hasattr(enum, "values"):
            raise EnumError("Enums need to inherit from Enum (not EnumMeta)!")

    @property
    def values(cls) -> list:
        """Returns all enum elements as a list"""

        elements = []
        for name, value in cls.__dict__.items():
            if not name.startswith("__") and type(value) != list:
                elements.append(value)
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
    elem1 = Class(arg1, arg2, ...)
    elem2 = Class(arg1, arg2, ...)
    ...

    Generates a enum with custom objects

    """
