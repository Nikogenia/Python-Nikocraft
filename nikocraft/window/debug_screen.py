# External modules
import pygame as pg

# Local modules
from ..constants import SCREEN_UPDATE_EVENT
from .window import Window
from .renderer import Renderer
from .rgb import RGB, RGBColor


class DebugScreen(Renderer):
    """Renderer class for a debug screen"""
    
    def __init__(self, window: Window, color: RGBColor = RGB.WHITE,
                 font_name: str = "calibri", font_system: bool = True) -> None:

        super(DebugScreen, self).__init__(window.screen)

        self.window: Window = window
        self.color: RGBColor = color
        self.font_name: str = font_name
        self.font_system: bool = font_system

        self.window.add_event_hook(f"Debug Screen - {id(self)}", SCREEN_UPDATE_EVENT,
                                   lambda *args: setattr(self, "surface", self.window.screen))

    def render(self) -> None:

        font = self.window.font.get(self.font_name, 25, self.font_system)

        self.surface.blit(font.render(f"{self.window.app.name}   v{self.window.app.version}   (by {self.window.app.author})", True, self.color), (0, 0))
        self.surface.blit(font.render(f"FPS: {self.window.clock.available_fps:.3f} ({self.window.clock.real_fps:.3f})", True, self.color), (0, 35))
        self.surface.blit(font.render(f"Delta Time: {self.window.clock.delta_time_raw*1000:.1f} ms ({self.window.clock.delta_time:.3f})", True, self.color), (0, 60))
        self.surface.blit(font.render(f"Timings: {self.window.clock.frame_durations[-1]*1000:.2f} ms", True, self.color), (0, 85))
        self.surface.blit(font.render(f"   Event: {self.window.stat_event_time*1000:.2f} ms", True, self.color), (0, 110))
        self.surface.blit(font.render(f"   Render: {self.window.stat_render_time*1000:.2f} ms", True, self.color), (0, 135))
        self.surface.blit(font.render(f"   Update: {self.window.stat_update_time*1000:.2f} ms", True, self.color), (0, 160))
        self.surface.blit(font.render(f"   Early Update: {self.window.stat_e_update_time*1000:.2f} ms", True, self.color), (0, 185))
        self.surface.blit(font.render(f"   Late Update: {self.window.stat_l_update_time*1000:.2f} ms", True, self.color), (0, 210))
        self.surface.blit(font.render(f"Screen: {self.window.width} x {self.window.height} px", True, self.color), (0, 245))
