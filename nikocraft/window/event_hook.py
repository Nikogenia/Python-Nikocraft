# Standard modules
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

# External modules
import pygame as pg

# Local modules
if TYPE_CHECKING:
    from .window import Window


@dataclass(frozen=True)
class EventHook:
    """Event hook dataclass"""

    name: str
    events: tuple[int, ...]
    handlers: tuple[Callable[[pg.event.Event, Window, dict], None], ...]
    data: dict
