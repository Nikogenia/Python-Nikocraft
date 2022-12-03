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
        __enum = super().__new__(mcs, name, bases, attrs)

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

    # OVERLOADS

    def __setattr__(cls, key, value):
        if "__build__" not in vars(cls):
            raise EnumError("Changing enum elements is not allowed!")
        super().__setattr__(key, value)

    def __delattr__(cls, key):
        if "__build__" not in vars(cls):
            raise EnumError("Deleting enum elements is not allowed!")
        super().__delattr__(key)

    def __contains__(cls, item):
        try:
            return item in getattr(cls, "values")
        except (IndexError, TypeError, KeyError):
            return False

    def __iter__(cls):
        return iter(getattr(cls, "values"))

    def __len__(cls):
        return len(getattr(cls, "values"))

    def __getitem__(cls, item):
        if item not in cls:
            raise EnumError(f"Cannot find '{item}' in '{cls}'!")
        return getattr(cls, item)

    def __setitem__(cls, item, value):
        raise EnumError("Changing enum elements is not allowed!")

    def __delitem__(cls, item):
        raise EnumError("Deleting enum elements is not allowed!")

    def __call__(cls, element: str):
        if element not in cls:
            raise EnumError(f"Cannot find '{element}' in '{cls}'!")
        return getattr(cls, element)

    # PROPERTIES

    @property
    def values(cls) -> list:
        """Returns all enum elements as a list"""
        return [value for name, value in vars(cls).items() if not name.startswith("__") and name != "values"]


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
