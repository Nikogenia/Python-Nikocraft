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


class App(ABC):
    """Main class of the application"""

    _initialized = False

    def __init__(self, args: list[str] = None, *, name: str = "Sample Project", author: str = "Nikocraft",
                 version: str = "0.0.1", short_description: str = "A short description",
                 description: str = "This is a sample project for the nikocraft library ...",
                 details: str = "Some more details ...", log_path: str = "./logs", log_thread: bool = False) -> None:

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

        self.exit_code: int = 0

        file.make_dir(self.log_path)

        log_files = []
        for entry in os.listdir(self.log_path):
            if file.is_file(file.join(self.log_path, entry)):
                if file.file_type(entry) == "log":
                    log_files.append(entry)
        if len(log_files) > 10:
            for i in range(10, len(log_files)):
                os.remove(file.join(self.log_path, log_files[i - 10]))

        self.head = f"{self.name.upper()}\n{'-' * len(self.name)}\n\n{self.short_description}\n\nDESCRIPTION\n{self.description}\n\n" \
                    f"DETAILS\nVersion: {self.version}\nAuthor: {self.author}\nFramework: Nikocraft (v{VERSION})\n{self.details}\n"
        print(self.head)
        with file.open_utf8(self.log_file, "w") as f:
            f.write(self.head + "\n")

        self.log_format = logging.Formatter(f"[%(asctime)s] [%(name)s{' - %(threadName)s' if self.log_thread else ''}] [%(levelname)s] %(message)s", '%d/%b/%y %H:%M:%S')
        self.log_handler_file = logging.FileHandler(self.log_file, encoding="utf-8")
        self.log_handler_console = logging.StreamHandler(sys.stdout)
        self.log_handler_file.setFormatter(self.log_format)
        self.log_handler_console.setFormatter(self.log_format)
        self.logger = logging.Logger(self.name.upper(), logging.DEBUG if self.debug else logging.INFO)
        self.logger.addHandler(self.log_handler_file)
        self.logger.addHandler(self.log_handler_console)

        self.logger.info(f"Debug Mode: {'On' if self.debug else 'Off'}")
        self.logger.info(f"Run Path: {os.path.abspath('.')}")

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
