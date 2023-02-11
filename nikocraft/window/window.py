"""Contains the window class for GUI management"""

# Standard modules
from typing import Callable, Self
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
from .rgb import RGB
from .clock import Clock
from .font import FontManager
from .event_hook import EventHook
from .scene import Scene
from .surface_interface import SurfaceInterface


class Window(SurfaceInterface):
    """Window class for the GUI management"""

    _initialized = False

    def __init__(self, app: App, *, fps: int = DEFAULT_FPS,
                 width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                 flags: int = 0, auto_update_screen: bool = True, auto_quit: bool = True,
                 scene_mode: bool = False, start_scene: str = "", start_scene_args: dict = None) -> None:

        super(Window, self).__init__("screen")

        # App
        self.app = app

        # Initialize
        self.logger.info("Initialize window ...")

        # General information
        self.screen: pg.Surface = pg.Surface((0, 0))
        self.target_dimension: Vec = Vec(width, height)
        self.running: bool = False
        self.clock: Clock = Clock(fps)
        self.flags: int = flags
        self.auto_update_screen: bool = auto_update_screen
        self.auto_quit: bool = auto_quit

        # Statistics
        self.stat_event_time: float = 0
        self.stat_render_time: float = 0
        self.stat_e_update_time: float = 0
        self.stat_update_time: float = 0
        self.stat_l_update_time: float = 0
        self.stat_other_time: float = 0

        # Scene management
        self.scene_mode: bool = scene_mode
        self.start_scene: str = start_scene
        self.start_scene_args: dict = {} if start_scene_args is None else start_scene_args
        self.scene: Scene | None = None
        self.next_scene_name: str = ""
        self.next_scene_args: dict = {}
        self.transition_duration: int = 0
        self.transition_tick: float = -1
        self.transition_surface: pg.Surface = pg.Surface((0, 0))
        self.scene_index: dict[str, type] = {}

        # Initialize pygame
        pg.init()

        # Initialize font manager
        self.font: FontManager = FontManager()

        # Event hooks
        self._event_hook_id = 0
        self.event_hooks: list[EventHook] = []

        # Set initialized flag
        self._initialized = True

    # PROPERTIES

    @property
    def logger(self) -> logging.Logger:
        return self.app.logger

    @property
    def dt(self) -> float:
        return self.clock.delta_time

    # METHODS

    def open(self) -> None:
        """Open the window

        *Returns nothing*
        """

        # Check for initialization
        assert self._initialized, "Window was not initialized!"

        # Open window
        self.logger.info("Open window ...")
        self.screen: pg.Surface = pg.display.set_mode(self.target_dimension, self.flags)
        self.init()

        # Load start scene
        if self.scene_mode:
            if self.start_scene == "":
                if not self.scene_index:
                    raise ValueError("Empty scene index! Register scenes to use the scene mode ...")
                self.scene: Scene | None = tuple(self.scene_index.values())[0](self, self.start_scene_args)
            else:
                if self.start_scene not in self.scene_index:
                    raise KeyError("Missing scene in index! Register scenes to use the scene mode ...")
                self.scene: Scene | None = self.scene_index[self.start_scene](self, self.start_scene_args)
            self.scene.activate_event_hooks()
            self.scene.init()

        # Window loop
        self.running = True
        while self.running:

            # Clock tick
            self.clock.tick()

            # Early update
            benchmark = time.benchmark()
            self.early_update()
            if self.scene_mode:
                self.scene.early_update()
            self.stat_e_update_time = benchmark()

            # Event handling
            benchmark = time.benchmark()
            for event in pg.event.get():

                # Window event handler
                self.event(event)

                # Scene event handler
                if self.scene_mode:
                    self.scene.event(event)

                # Event hooks
                for hook in self.event_hooks:
                    if event.type in hook.events:
                        for handler in hook.handlers:
                            handler(event, self, hook.data)

                # Default event handlers
                if event.type == pg.QUIT and self.auto_quit:
                    self.running = False
            self.stat_event_time = benchmark()

            # Update
            benchmark = time.benchmark()
            self.update()
            if self.scene_mode:
                self.scene.update()
            self.stat_update_time = benchmark()

            # Screen rendering
            benchmark = time.benchmark()
            self.render()
            if self.auto_update_screen:
                pg.display.flip()
            self.stat_render_time = benchmark()

            # Late update
            benchmark = time.benchmark()
            self.late_update()
            if self.scene_mode:
                self.scene.late_update()
            self.stat_l_update_time = benchmark()

            # Transition updating
            if self.transition_tick != -1:
                self.transition_tick += self.dt
            if self.next_scene_name != "" and self.transition_tick >= self.transition_duration:
                self.scene.quit()
                self.scene.deactivate_event_hooks()
                self.scene: Scene | None = self.scene_index[self.next_scene_name](self, self.next_scene_args)
                self.next_scene_name = ""
                self.next_scene_args = {}
                self.scene.activate_event_hooks()
                self.scene.init()
            if self.transition_tick != -1 and self.transition_tick >= self.transition_duration * 2:
                self.transition_duration = 0
                self.transition_tick = -1

        # Shutdown
        self.logger.info("Close window ...")
        if self.scene_mode:
            self.scene.quit()
            self.scene.deactivate_event_hooks()
        self.quit()
        pg.quit()

    def add_event_hook(self, event: int | tuple[int, ...], handler: tuple[Callable[[pg.event.Event, Self, dict], None], ...] |
                       Callable[[pg.event.Event, Self, dict], None], data: dict = None) -> EventHook:
        """Add a new event hook"""

        hook = EventHook(self._event_hook_id, event if isinstance(event, tuple) else (event,),
                         handler if isinstance(handler, tuple) else (handler,), data if data is not None else {})
        self._event_hook_id += 1
        self.event_hooks.append(hook)
        return hook

    def remove_event_hook(self, hook_id: int) -> bool:
        """Remove a event hook"""

        for hook in self.event_hooks:
            if hook.id == hook_id:
                self.event_hooks.remove(hook)
                return True
        return False

    def change_scene(self, name: str, args: dict = None, transition_duration: int = 10) -> None:
        """Change the scene"""

        self.logger.info(f"Switch scene to '{name}' with duration of {transition_duration} ...")
        self.logger.debug(f"Scene arguments: {args}")

        self.next_scene_name = name
        self.next_scene_args = {} if args is None else args
        self.transition_duration = transition_duration
        self.transition_tick = 0

    def register_scene(self, name: str, scene_class: type) -> None:
        """Register a new scene"""

        self.scene_index[name] = scene_class

    def get_scene_name(self, scene: Scene) -> str:
        """Get the name of a scene"""

        for name, scene_class in self.scene_index.items():
            if isinstance(scene, scene_class):
                return name

    def render_scene(self) -> None:
        """Render the scene and transition"""

        self.scene.render()

        if self.transition_tick != -1 and self.transition_duration != 0:

            if self.transition_surface.get_width() != self.width or self.transition_surface.get_height() != self.width:
                self.transition_surface: pg.Surface = pg.Surface(self.dimension)
                self.transition_surface.fill(RGB.BLACK)

            if self.transition_tick < self.transition_duration:
                self.transition_surface.set_alpha(int(255 * (self.transition_tick / self.transition_duration)))
            else:
                self.transition_surface.set_alpha(int(255 - 255 * ((self.transition_tick - self.transition_duration) / self.transition_duration)))

            self.screen.blit(self.transition_surface, (0, 0))

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
