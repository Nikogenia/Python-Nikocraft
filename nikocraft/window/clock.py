"""Contains the clock class for time handling in pygame"""

# External modules
import pygame as pg

# Local modules
from ..utils import time


class Clock:
    """Clock class for time handling in pygame"""

    def __init__(self, max_fps: int) -> None:

        # Limiting
        self.max_fps: int = max_fps
        self.limiter: pg.time.Clock = pg.time.Clock()

        # Statistics
        self.start_time: float = 0
        self.frame_count: int = 0
        self.frame_start: float = 0
        self.frame_end: float = 0
        self.frame_durations: list[float] = [0] * 90
        self.frame_duration: float = 1
        self.frame_duration_low: float = 1
        self.frame_duration_lazy: float = 1
        self.last_update: float = 0

        # Delta time
        self.delta_time_raw: float = 0
        self.delta_time: float = 0
        self.last_time: float = 0

        # Manipulation
        self.speed_factor: float = 1

    # PROPERTIES

    @property
    def real_fps(self) -> float:
        return round(self.limiter.get_fps(), 5)

    @property
    def available_fps(self) -> float:
        return round(1 / self.frame_duration, 5)

    @property
    def available_fps_low(self) -> float:
        return round(1 / self.frame_duration_low, 5)

    @property
    def available_fps_lazy(self) -> float:
        return round(1 / self.frame_duration_lazy, 5)

    # METHODS

    def tick(self, max_fps: int = None) -> None:
        """Next frame (Calculates statistics and delta time and waits until the next frame should be calculated)"""

        # Statistics
        self.frame_end: float = time.bench_time()
        self.frame_durations.append(self.frame_end - self.frame_start)
        del self.frame_durations[0]

        if time.bench_time() - self.last_update > 0.2:

            self.frame_duration: float = sum(self.frame_durations[-5:]) / 5
            if self.frame_duration == 0:
                self.frame_duration: float = 1

            low_list: list[float] = []
            duration_copy: list[float] = self.frame_durations.copy()
            while len(low_list) < 3:
                value = max(duration_copy)
                duration_copy.remove(value)
                low_list.append(value)
            self.frame_duration_low: float = sum(low_list) / 3
            if self.frame_duration_low == 0:
                self.frame_duration_low: float = 1

            self.frame_duration_lazy: float = sum(self.frame_durations) / len(self.frame_durations)
            if self.frame_duration_lazy == 0:
                self.frame_duration: float = 1

            self.last_update: float = time.bench_time()

        # Limiting
        if max_fps is not None:
            self.max_fps: int = max_fps
        self.limiter.tick(self.max_fps)

        # Delta time
        if self.last_time == 0:
            self.delta_time_raw: float = 1 / self.max_fps
        else:
            self.delta_time_raw: float = time.bench_time() - self.last_time
        self.last_time: float = time.bench_time()
        self.delta_time = self.delta_time_raw * self.max_fps * self.speed_factor

        # Statistics
        self.frame_count += 1
        self.frame_start: float = time.bench_time()

    # OVERLOADS

    def __repr__(self) -> str:
        return f"Clock[id={id(self)}, real_fps={self.real_fps}, available_fps={self.available_fps}, max_fps={self.max_fps}, speed_factor={self.speed_factor}, frame_count={self.frame_count}]"
