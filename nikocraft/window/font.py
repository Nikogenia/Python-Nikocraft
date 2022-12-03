# External modules
import pygame as pg


class FontManager:
    """Font manager class"""
    
    def __init__(self) -> None:

        self.fonts = {}
        self.cache = {}

    def define(self, name: str, path: str) -> None:
        """Define a new font"""
        self.fonts[name] = path

    def get(self, name: str, size: int, system: bool = False) -> pg.font.Font:
        """Get a font"""

        # Check for cache
        if name in self.cache:
            if size in self.cache[name]:
                return self.cache[name][size]

        # Load font
        if system:
            font = pg.font.SysFont(name, size)
        else:
            font = pg.font.Font(self.fonts[name], size)

        # Store to cache
        if name not in self.cache:
            self.cache[name] = {}
        self.cache[name][size] = font

        # Return cache
        return font
