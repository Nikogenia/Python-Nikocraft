"""Contains the window class for GUI management"""

# Standard modules
from abc import ABC, abstractmethod
import os
import ctypes

# External modules
import pygame as pg

# Local modules
from ..constants import *
from ..app import App
from .vector2d import Vec


class Window(ABC):
    """Window class for the GUI management"""

    _initialized = False

    def __init__(self, app: App) -> None:

        self.screen: pg.Surface = pg.Surface((0, 0))
        self.target_dimension = Vec(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.running: bool = False
        self.max_fps = DEFAULT_FPS
        self.flags: int = 0

        pg.init()

        self._initialized = True

    @property
    def width(self):
        return self.screen.get_width()

    @property
    def height(self):
        return self.screen.get_height()

    @property
    def dimension(self):
        return Vec(self.screen.get_width(), self.screen.get_height())

    def open(self) -> None:
        """Open the window

        *Returns nothing*
        """

        assert self._initialized, "Application was not initialized!"

        self.screen = pg.display.set_mode(self.target_dimension, self.flags)

        while self.running:
            break

        self.quit()
        pg.quit()

    @abstractmethod
    def event(self, event: pg.event.Event) -> None:
        """Handle pygame event

        *Called when event is fired*
        """

        pass

    @abstractmethod
    def render(self) -> None:
        """Render screen

        *Called every frame*
        """

        pass

    @abstractmethod
    def quit(self) -> None:
        """Shutdown tasks

        *Called before closing -
        Don't call this method manually*
        """

        pass
