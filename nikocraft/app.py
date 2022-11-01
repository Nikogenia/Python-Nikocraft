"""Contains the main class of the application"""

# Standard modules
from abc import ABC, abstractmethod
from typing import AnyStr
import os
import sys
import ctypes

# External modules


# Local modules
from .constants import *


class App(ABC):
    """Main class of the application"""

    _initialized = False

    def __init__(self, args: list[AnyStr] = None) -> None:

        self.args: list[AnyStr] = args if args else sys.argv
        self.debug: bool = "-d" in args or "--debug" in args

        self.exit_code: int = 0

        self._initialized: bool = True

    def start(self) -> int:
        """Start the application

        Returns the exit code
        """

        assert self._initialized, "Application was not initialized!"

        self.run()

        self.quit()
        return self.exit_code

    @abstractmethod
    def run(self) -> None:
        """Application execution

        Called on starting -
        Don't call this method manually
        """

        pass

    @abstractmethod
    def quit(self) -> None:
        """Shutdown tasks

        Called before exiting -
        Don't call this method manually
        """

        pass

    @staticmethod
    def disable_resolution_scaling() -> None:
        """Disable resolution scaling on Windows

        Returns nothing
        """

        if os.name == "nt":
            ctypes.windll.user32.SetProcessDPIAware()
