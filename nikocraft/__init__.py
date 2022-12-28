"""Nikocraft Python Library"""

# Environment variables
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
del os

# Modules
from .utils import time
from .utils import file
from .utils import log

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
from .window.renderer import Renderer
from .window.debug_screen import DebugScreen
from .window.event_hook import EventHook
from .window.scene import Scene

# Constants
from .constants import AUTHOR, VERSION, CUSTOM_EVENT, SCREEN_UPDATE_EVENT, Transition

__all__ = [
    "time",
    "file",
    "log",
    "App",
    "Config",
    "Enum",
    "Window",
    "Vec",
    "Vec3",
    "RGB",
    "RGBColor",
    "Clock",
    "Renderer",
    "DebugScreen",
    "EventHook",
    "Scene",
    "AUTHOR",
    "VERSION",
    "CUSTOM_EVENT",
    "SCREEN_UPDATE_EVENT",
    "Transition"
]
