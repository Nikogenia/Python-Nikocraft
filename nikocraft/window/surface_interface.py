# Local modules
from .vector2d import Vec


class SurfaceInterface:
    """Pygame surface interface class"""
    
    def __init__(self, surface_name: str) -> None:

        self.surface_name = surface_name

    # PROPERTIES

    @property
    def width(self) -> int:
        return getattr(self, self.surface_name).get_width()

    @property
    def height(self) -> int:
        return getattr(self, self.surface_name).get_height()

    @property
    def dimension(self) -> Vec:
        surface = getattr(self, self.surface_name)
        return Vec(surface.get_width(), surface.get_height())
