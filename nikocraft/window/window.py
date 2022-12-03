"""Contains the window class for GUI management"""

# Standard modules
from abc import ABC
import os
import ctypes

# External modules
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame as pg

# Local modules
from ..constants import *
from ..app import App
from .vector2d import Vec
from .clock import Clock


class Window(ABC):
    """Window class for the GUI management"""

    _initialized = False

    def __init__(self, app: App) -> None:

        # App
        self.app = app

        # General information
        self.screen: pg.Surface = pg.Surface((0, 0))
        self.target_dimension: Vec = Vec(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.running: bool = False
        self.clock: Clock = Clock(DEFAULT_FPS)
        self.flags: int = 0
        self.option_auto_update_screen: bool = True
        self.option_auto_quit: bool = True

        # Initialize pygame
        pg.init()

        # Set initialized flag
        self._initialized = True

    # PROPERTIES

    @property
    def width(self):
        return self.screen.get_width()

    @property
    def height(self):
        return self.screen.get_height()

    @property
    def dimension(self):
        return Vec(self.screen.get_width(), self.screen.get_height())

    # METHODS

    def open(self) -> None:
        """Open the window

        *Returns nothing*
        """

        # Check for initialization
        assert self._initialized, "Window was not initialized!"

        # Open window
        self.screen: pg.Surface = pg.display.set_mode(self.target_dimension, self.flags)
        self.init()

        # Window loop
        self.running = True
        while self.running:

            # Clock tick
            self.clock.tick()

            # Event handling
            for event in pg.event.get():
                self.event(event)
                if event.type == pg.QUIT and self.option_auto_quit:
                    self.running = False

            # Screen rendering
            self.render()
            if self.option_auto_update_screen:
                pg.display.flip()

        # Shutdown
        self.quit()
        pg.quit()

    # ABSTRACT METHODS

    def init(self) -> None:
        """Startup tasks

        *Called after window is opened -
        Don't call this method manually*
        """

        pass

    def event(self, event: pg.event.Event) -> None:
        """Handle pygame event

        *Called when event is fired*
        """

        pass

    def render(self) -> None:
        """Render screen

        *Called every frame*
        """

        pass

    def quit(self) -> None:
        """Shutdown tasks

        *Called before closing -
        Don't call this method manually*
        """

        pass

    # STATIC METHODS

    @staticmethod
    def disable_resolution_scaling() -> None:
        """Disable resolution scaling on Windows

        Returns nothing
        """

        if os.name == "nt":
            ctypes.windll.user32.SetProcessDPIAware()
