# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod
import json

# -----------------------------------------------------------------------------
# InfoBase
# -----------------------------------------------------------------------------
class InfoBase(ABC):
    def __init__(self):
        ...

    @classmethod
    @abstractmethod
    def from_file(cls, file_path):
        """
        Load configuration from a file.
        """
        ...

    @classmethod
    @abstractmethod
    def from_json(cls, json_str):
        """
        Load configuration from a JSON string.
        """
        ...

    @abstractmethod
    def to_json(self):
        """
        Convert the configuration to a JSON string.
        """
        ...

    @abstractmethod
    def print_info(self):
        """
        Print the configuration information.
        """
        ...