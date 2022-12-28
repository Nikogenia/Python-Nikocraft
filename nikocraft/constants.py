# Enum
from enum import StrEnum, auto


# Credits
VERSION = "0.0.2"
AUTHOR = "Nikocraft"

# Window
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 700
DEFAULT_FPS = 30

# Custom Event
CUSTOM_EVENT = 40000
SCREEN_UPDATE_EVENT = CUSTOM_EVENT + 1


# Transition
class Transition(StrEnum):

    INSTANT = auto()

    BLEND = auto()

    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()


# Clear namespace
del StrEnum, auto
