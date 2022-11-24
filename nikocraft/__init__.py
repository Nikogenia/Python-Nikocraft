"""Nikocraft Python Library"""

# Environment variables
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
del os

# Modules
from .utils import time
from .utils import file

# Classes
from .app import App
from .utils.config import Config
from .utils.enum import Enum
from .window.window import Window
from .window.vector2d import Vec
from .window.vector3d import Vec3
from .window.rgb import RGB
from .window.rgb import RGBColor
from .window.clock import Clock

# Constants
from .constants import AUTHOR, VERSION

__all__ = [
    "time",
    "App",
    "Config",
    "Enum",
    "Window",
    "Vec",
    "Vec3",
    "RGB",
    "RGBColor",
    "Clock",
    "AUTHOR",
    "VERSION"
]
