"""Contains the main class of the application"""

# Standard modules
from abc import ABC, abstractmethod
import logging
import os
import sys

# External modules

# Local modules
from .constants import *
from .utils import time
from .utils import file
from .utils import log


class App(ABC):
    """Main class of the application"""

    _initialized = False

    def __init__(self, args: list[str] = None, *, name: str = "Sample Project", author: str = "Nikocraft",
                 version: str = "0.0.1", short_description: str = "A short description",
                 description: str = "This is a sample project for the nikocraft library ...",
                 details: str = "Some more details ...", log_path: str = "./logs",
                 log_thread: bool = False, log_date: bool = True) -> None:

        # General information
        self.args: list[str] = args if args else sys.argv
        self.debug: bool = "-d" in self.args or "--debug" in self.args
        self.name: str = name
        self.author: str = author
        self.version: str = version
        self.short_description: str = short_description
        self.description: str = description
        self.details: str = details
        self.log_path: str = log_path
        self.log_file: str = f"{self.log_path}/log_{time.datetime_f_ymd_hms()}.log"
        self.log_thread: bool = log_thread
        self.log_date: bool = log_date

        # Exit information
        self.exit_code: int = 0

        # Setup logging
        log.setup_log_directory(self.log_path)
        self.head = f"{self.name.upper()}\n{'-' * len(self.name)}\n\n{self.short_description}\n\nDESCRIPTION\n{self.description}\n\n" \
                    f"DETAILS\nVersion: {self.version}\nAuthor: {self.author}\nFramework: Nikocraft (v{VERSION})\n{self.details}\n"
        log.setup_log_file(self.log_file, self.head)
        self.logger = log.create_logger(self.log_file, self.name.upper(), logging.DEBUG if self.debug else logging.INFO, log_thread=log_thread, log_date=log_date)

        # Log runtime information
        self.logger.info(f"Debug Mode: {'On' if self.debug else 'Off'}")
        self.logger.info(f"Run Path: {os.path.abspath('.')}")

        # Set initialized flag
        self._initialized: bool = True

    def start(self) -> int:
        """Start the application

        Returns the exit code
        """

        # Check for initialization
        assert self._initialized, "Application was not initialized!"

        # Run application
        self.run()

        # Shutdown tasks
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
