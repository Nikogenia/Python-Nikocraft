# Local modules
from ..constants import SCREEN_UPDATE_EVENT
from .window import Window
from .renderer import Renderer
from .rgb import RGB


class DebugScreen(Renderer):
    """Renderer class for a debug screen"""
    
    def __init__(self, window: Window) -> None:

        super(DebugScreen, self).__init__(window.screen)

        self.window = window

        self.window.add_event_hook(f"DebugScreenSurfaceUpdate-{id(self)}", SCREEN_UPDATE_EVENT, lambda *args: setattr(self, "surface", self.window.screen))

    def render(self) -> None:

        font = self.window.font.get("calibri", 25, True)

        self.surface.blit(font.render(f"{self.window.app.name}   v{self.window.app.version}   (by {self.window.app.author})", True, RGB.WHITE), (0, 0))
        self.surface.blit(font.render(f"FPS: {self.window.clock.available_fps:.3f} ({self.window.clock.real_fps:.3f})", True, RGB.WHITE), (0, 35))
        self.surface.blit(font.render(f"Delta Time: {self.window.clock.delta_time_raw:.3f} ms ({self.window.clock.delta_time:.3f})", True, RGB.WHITE), (0, 60))
        self.surface.blit(font.render(f"Timings: {self.window.clock.frame_durations[-1]:.5f} ms", True, RGB.WHITE), (0, 85))
        self.surface.blit(font.render(f"   Event: {self.window.stat_event_time:.5f} ms", True, RGB.WHITE), (0, 110))
        self.surface.blit(font.render(f"   Render: {self.window.stat_render_time:.5f} ms", True, RGB.WHITE), (0, 135))
        self.surface.blit(font.render(f"   Other: {self.window.stat_other_time:.5f} ms", True, RGB.WHITE), (0, 160))
        self.surface.blit(font.render(f"Screen: {self.window.width} x {self.window.height} px", True, RGB.WHITE), (0, 195))

