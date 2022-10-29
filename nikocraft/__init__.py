"""Nikocraft Python Library"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

from .app import App
from . import window
from .window.vector2d import Vec
from .constants import AUTHOR, VERSION

__all__ = [
    "App",
    "AUTHOR",
    "VERSION",
    "window",
    "Vec"
]

del os
