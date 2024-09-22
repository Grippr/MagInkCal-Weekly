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
        ...

    @classmethod
    def from_json(cls, json_str):
        ...

    def to_json(cls, json_str):
        ...

    @abstractmethod
    def log_info(self):
        """
        Log the configuration information.
        """
        ...