"""Contains the window class for GUI management"""

# Standard modules
from typing import Callable, Self
from abc import ABC
import os
import ctypes
import logging

# External modules
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame as pg

# Local modules
from ..constants import *
from ..app import App
from ..utils import time
from .vector2d import Vec
from .clock import Clock
from .font import FontManager
from .event_hook import EventHook


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

        # Statistics
        self.stat_event_time: float = 0
        self.stat_render_time: float = 0
        self.stat_other_time: float = 0

        # Initialize pygame
        pg.init()

        # Initialize font manager
        self.font: FontManager = FontManager()

        # Event hooks
        self.event_hooks: list[EventHook] = []

        # Set initialized flag
        self._initialized = True

    # PROPERTIES

    @property
    def logger(self) -> logging.Logger:
        return self.app.logger

    @property
    def width(self) -> int:
        return self.screen.get_width()

    @property
    def height(self) -> int:
        return self.screen.get_height()

    @property
    def dimension(self) -> Vec:
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
        pg.event.post(pg.event.Event(SCREEN_UPDATE_EVENT))
        self.init()

        # Window loop
        self.running = True
        while self.running:

            # Clock tick
            self.clock.tick()

            # Event handling
            with time.benchmark(lambda result: setattr(self, "stat_event_time", result)):
                for event in pg.event.get():

                    # Window event handler
                    self.event(event)

                    # Event hooks
                    for hook in self.event_hooks:
                        for event_type in hook.events:
                            if event.type == event_type:
                                for handler in hook.handlers:
                                    handler(event, self, hook.data)
                                break

                    # Default event handlers
                    if event.type == pg.QUIT and self.option_auto_quit:
                        self.running = False

            # Screen rendering
            with time.benchmark(lambda result: setattr(self, "stat_render_time", result)):
                self.render()
                if self.option_auto_update_screen:
                    pg.display.flip()

            # Statistics
            self.stat_other_time: float = self.clock.frame_durations[-1] - self.stat_event_time - self.stat_render_time
            if self.stat_other_time < 0:
                self.stat_other_time = 0

        # Shutdown
        self.quit()
        pg.quit()

    def add_event_hook(self, name: str, event: int | tuple[int, ...], handler: tuple[Callable[[pg.event.Event, Self, dict], None], ...] |
                       Callable[[pg.event.Event, Self, dict], None], data: dict = None) -> EventHook:
        """Add a new event hook"""
        hook = EventHook(name, event if isinstance(event, tuple) else (event,),
                         handler if isinstance(handler, tuple) else (handler,), data if data is not None else {})
        self.event_hooks.append(hook)
        return hook

    def remove_event_hook(self, name: str) -> bool:
        """Remove a event hook"""
        for hook in self.event_hooks:
            if hook.name == name:
                self.event_hooks.remove(hook)
                return True
        return False

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
