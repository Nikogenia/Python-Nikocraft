# External modules
import pygame as pg

# Local modules
from .window import Window
from .surface_interface import SurfaceInterface
from .rgb import RGB, RGBColor


class DebugScreen(SurfaceInterface):
    """Renderer class for a debug screen"""
    
    def __init__(self, window: Window, color: RGBColor = RGB.WHITE,
                 font_name: str = "calibri", font_system: bool = True,
                 font_size: int = 22, font_antialias: bool = True) -> None:

        super(DebugScreen, self).__init__("screen")

        self.window: Window = window
        self.color: RGBColor = color
        self.font_name: str = font_name
        self.font_system: bool = font_system
        self.font_size: int = font_size
        self.font_antialias: bool = font_antialias

    # PROPERTIES

    @property
    def screen(self) -> pg.Surface:
        return self.window.screen

    # METHODS

    def render(self, left_content: list[str] = None) -> None:

        font = self.window.font.get(self.font_name, self.font_size, self.font_system)
        height = font.get_height()

        if left_content is None:
            left_content = self.left_content()

        y = 0
        for line in left_content:
            if line != "":
                self.screen.blit(font.render(line, self.font_antialias, self.color), (0, y))
                y += height
            else:
                y += 10

    def left_content(self) -> list[str]:

        win = self.window

        return [
            f"{win.app.name}   v{win.app.version}   (by {win.app.author})",
            f"",
            f"FPS: {win.clock.available_fps:.3f} ({win.clock.real_fps:.3f})",
            f"Delta Time: {win.clock.delta_time_raw*1000:.1f} ms ({win.clock.delta_time:.3f})",
            f"Timings: {win.clock.frame_durations[-1]*1000:.2f} ms",
            f"   Event: {win.stat_event_time*1000:.2f} ms",
            f"   Render: {win.stat_render_time*1000:.2f} ms",
            f"   Update: {win.stat_update_time*1000:.2f} ms",
            f"   Early Update: {win.stat_e_update_time*1000:.2f} ms",
            f"   Late Update: {win.stat_l_update_time*1000:.2f} ms",
            f"",
            f"Screen: {win.width} x {win.height} px",
            f"",
            f"Scene: {type(win.scene).__name__ if win.scene_mode else '<off>'}"
        ]
