# External modules
import pygame as pg

# Local modules
from .vector2d import Vec


class Renderer:
    """Pygame surface renderer class"""
    
    def __init__(self, surface: pg.Surface) -> None:

        self.surface = surface

    # PROPERTIES

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()

    @property
    def dimension(self) -> Vec:
        return Vec(self.surface.get_width(), self.surface.get_height())

    # ABSTRACT METHODS

    def render(self) -> None:
        """Render the surface"""

        pass

    def update(self) -> None:
        """Update tasks"""

        pass
