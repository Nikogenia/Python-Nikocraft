# Standard modules
from abc import ABC, abstractmethod
from typing import Self

# External modules
import pygame as pg

# Local modules
from .vector2d import Vec


class Renderer(ABC):
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

    # METHODS

    def change(self, surface: pg.Surface) -> None:
        """Change the current surface"""
        self.surface = surface

    # CLASS METHODS

    @classmethod
    def cached(cls, width: int, height: int) -> Self:
        """Create a renderer with a new surface"""
        return cls(pg.Surface((width, height)))

    # ABSTRACT METHODS

    @abstractmethod
    def render(self) -> None:
        """Render the surface

        *Returns nothing*
        """

        pass
