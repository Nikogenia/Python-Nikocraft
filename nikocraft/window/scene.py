# Standard modules
from __future__ import annotations
from typing import TYPE_CHECKING, Self, Callable
import logging

# External modules
import pygame as pg

# Local modules
if TYPE_CHECKING:
    from .window import Window
from .surface_interface import SurfaceInterface
from .event_hook import EventHook


class Scene(SurfaceInterface):
    """Scene class"""

    def __init__(self, window: Window, args: dict = None) -> None:

        super(Scene, self).__init__("screen")

        self.window: Window = window
        self.args: dict = {} if args is None else args

        self.event_hooks: list[EventHook] = []

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

    # METHODS

    def add_event_hook(self, event: int | tuple[int, ...], handler: tuple[Callable[[pg.event.Event, Self, dict], None], ...] |
                       Callable[[pg.event.Event, Self, dict], None], data: dict = None) -> EventHook:
        """Add a new event hook to the scene"""

        hook = self.window.add_event_hook(event, handler, data)
        self.event_hooks.append(hook)
        return hook

    def remove_event_hook(self, hook_id: int) -> bool:
        """Remove a event hook of the scene"""

        self.window.remove_event_hook(hook_id)

        for hook in self.event_hooks:
            if hook.id == hook_id:
                self.event_hooks.remove(hook)
                return True
        return False

    def activate_event_hooks(self) -> None:
        """Activate all event hooks of the scene"""

        for hook in self.event_hooks:
            for h in self.window.event_hooks:
                if h.id == hook.id:
                    break
            else:
                self.window.event_hooks.append(hook)

    def deactivate_event_hooks(self) -> None:
        """Deactivate all event hooks of the scene"""

        for hook in self.event_hooks:
            self.window.remove_event_hook(hook.id)

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
