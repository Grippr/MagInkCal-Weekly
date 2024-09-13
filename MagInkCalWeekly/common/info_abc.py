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
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    @abstractmethod
    def print_info(self):
        """
        Print the configuration information.
        """
        ...