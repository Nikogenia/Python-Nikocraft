# Standard modules
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

# External modules
import pygame as pg

# Local modules
if TYPE_CHECKING:
    from .window import Window
from .surface_interface import SurfaceInterface


class Scene(SurfaceInterface):
    """Scene class"""

    def __init__(self, window: Window, args: dict = None) -> None:

        super(Scene, self).__init__("screen")

        self.window: Window = window
        self.args: dict = {} if args is None else args

    # PROPERTIES

    @property
    def screen(self) -> pg.Surface:
        return self.window.screen

    @property
    def logger(self) -> logging.Logger:
        return self.window.app.logger

    @property
    def dt(self) -> float:
        return self.window.clock.delta_time

    # ABSTRACT METHODS

    def init(self) -> None:
        """Startup tasks

        *Called after is initialized -
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

    def early_update(self) -> None:
        """Early update tasks

        *Called every frame before event handling*
        """

        pass

    def update(self) -> None:
        """Normal update tasks

        *Called every frame before rendering*
        """

        pass

    def late_update(self) -> None:
        """Late update tasks

        *Called every frame after rendering*
        """

        pass

    def quit(self) -> None:
        """Shutdown tasks

        *Called before exiting scene -
        Don't call this method manually*
        """

        pass
