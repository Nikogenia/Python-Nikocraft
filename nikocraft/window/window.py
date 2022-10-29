"""Contains the window class for GUI management"""

# Standard modules
from abc import ABC, abstractmethod
import os
import ctypes

# External modules
import pygame as pg

# Local modules
from ..app import App


class Window(ABC):
    """Window class for the GUI management"""

    _initialized = False

    def __init__(self, app: App) -> None:

        self.screen: pg.Surface = pg.Surface((0, 0))
        self.target_resolution = ()
        self.running: bool = False
        self.flags: int = 0

        pg.init()

        pg.Vector2().y

        self._initialized = True

    def open(self) -> None:
        """Open the window

        *Returns nothing*
        """

        assert self._initialized, "Application was not initialized!"

        self.screen = pg.display.set_mode()

        while

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
