"""Contains the config class for saving JSON configurations"""

# Standard modules
from typing import Any
from abc import ABC
from logging import Logger

# Local modules
from ..utils import file


class Config(ABC):
    """Config class for saving JSON configurations"""

    def __init__(self, path: str, logger: Logger = None) -> None:

        self.path: str = path
        self.logger: Logger = logger

    # METHODS

    def load(self) -> None:
        """Load data from JSON file at path"""

        # Load file
        if self.logger:
            self.logger.info(f"Load configuration file at '{self.path}' ...")
        data = file.load_json(self.path, self.logger, create=False)

        # Decode data
        if self.logger:
            self.logger.debug("Decode configuration attributes ...")
        for attribute in vars(self):
            if attribute in ("path", "logger"):
                continue
            result = self.load_attribute(attribute, data)
            if result is None:
                if attribute in data:
                    setattr(self, attribute, data[attribute])
            else:
                setattr(self, attribute, result)

    def save(self) -> None:
        """Save data to JSON file at path"""

        # Encode data
        data = {}
        if self.logger:
            self.logger.debug("Encode configuration attributes ...")
        for attribute in vars(self):
            if attribute in ("path", "logger"):
                continue
            result = self.save_attribute(attribute, getattr(self, attribute), data)
            if result is None:
                data[attribute] = getattr(self, attribute)

        # Save file
        if self.logger:
            self.logger.info(f"Save configuration file at '{self.path}' ...")
        file.save_json(self.path, data, self.logger)

    # ABSTRACT METHODS

    def load_attribute(self, attribute: str, data: dict) -> Any | None:
        """Load an attribute from data (Return result or None for automatic loading)

        *Called on loading -
        Don't call this method manually*
        """

        pass

    def save_attribute(self, attribute: str, value: Any, data: dict) -> Any | None:
        """Save an attribute to data (Modify data or return None for automatic saving)

        *Called on saving -
        Don't call this method manually*
        """

        pass

    def load_extras(self, data: dict) -> None:
        """Additional loading tasks

        *Called on loading -
        Don't call this method manually*
        """

        pass

    def save_extras(self, data: dict) -> None:
        """Additional saving tasks

        *Called on saving -
        Don't call this method manually*
        """

        pass

    # OVERLOADS

    def __repr__(self) -> str:
        return f"Config[id={id(self)}, path={self.path}]"
