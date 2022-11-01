"""Nikocraft Python Library"""

# Environment variables
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
del os

# Modules
from . import window
from .utils import time
from .window import rgb

# Classes
from .app import App
from .utils.config import Config
from .window.vector2d import Vec
from .window.vector3d import Vec3

# Constants
from .constants import AUTHOR, VERSION

__all__ = [
    "window",
    "time",
    "rgb",
    "App",
    "Config",
    "Vec",
    "Vec3",
    "AUTHOR",
    "VERSION"
]
