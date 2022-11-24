"""Contains the config class for saving JSON configurations"""

# Standard modules
from typing import Any
from abc import ABC, abstractmethod
import json

# Local modules
from ..utils import time


class Config(ABC):
    """Config class for saving JSON configurations"""

    def __init__(self, path: str) -> None:

        self.path: str = path

    def load(self) -> None:
        """Load data from JSON file at path"""

        print(vars(self))

    @abstractmethod
    def load_attribute(self, attribute: str, data: dict) -> Any:
        """Load an attribute from data (Return result or None for automatic loading)

        *Called on loading -
        Don't call this method manually*
        """

        pass

    def __repr__(self) -> str:
        return f"Config[id={id(self)}, path={self.path}]"
