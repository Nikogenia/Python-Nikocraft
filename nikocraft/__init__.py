"""Nikocraft Python Library"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

from .app import App
from .constants import *

__all__ = [
    "App"
]

del os
