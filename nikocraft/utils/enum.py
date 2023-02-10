"""Contains the enum class and metaclass"""


class EnumError(Exception):
    """A error for invalid usage of enums"""
    pass


class EnumMeta(type):
    """The metaclass for an enum"""

    def __new__(mcs, name, bases, attrs):
        return super().__new__(mcs, name, bases, attrs)

    # OVERLOADS

    def __setattr__(cls, key, value):
        raise EnumError("Changing enum elements is not allowed!")

    def __delattr__(cls, key):
        raise EnumError("Deleting enum elements is not allowed!")

    def __contains__(cls, item):
        try:
            return item in getattr(cls, "values")
        except (IndexError, TypeError, KeyError):
            return False

    def __iter__(cls):
        return iter(getattr(cls, "values"))

    def __reversed__(cls):
        return reversed(getattr(cls, "values"))

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

    elem1 = Class(arg1, arg2, ...)
    elem2 = Class(arg1, arg2, ...)
    ...

    """
