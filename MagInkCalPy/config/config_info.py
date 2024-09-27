# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from argparse import ArgumentParser
from dataclasses import dataclass, fields, asdict, MISSING
import logging
import json5 as json # json5 is a superset of JSON that allows comments
import os
from pytz import timezone

# -----------------------------------------------------------------------------
# Calendar Config
# -----------------------------------------------------------------------------
@dataclass
class ConfigInfo():
    displayTZ: timezone
    thresholdHours: int
    maxEventsPerDay: int
    isDisplayToScreen: bool
    isShutdownOnComplete:bool
    batteryDisplayMode: int
    weekStartDay: int
    dayOfWeekText: list
    screenWidth: int
    screenHeight: int
    rotateAngle: int
    is24h: bool
    calendars: list
    privateDirectory: str
    credentialsFileName: str
    tokenFileName: str
    numWeeks: int
    calendarImagePath: str = None
    logger = logging.getLogger("MagInkCalPy:ConfigInfo")

    
    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def to_json(self):
        return json.dumps(asdict(self))

    def log_info(self):
        for field in fields(self):
            value = getattr(self, field.name)
            self.logger.info(f"{field.name}: {value}")
    
    # CalendarInfo Utilities
    def get_credential_path(self):
        return os.path.join(self.privateDirectory, self.credentialsFileName)

    def get_token_path(self):
        return os.path.join(self.privateDirectory, self.tokenFileName)
    
    def get_tz(self):
        return timezone(self.displayTZ)
   
    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(
            "-c", "--config", 
            help="Path to the config file", 
            default="config.json5"
        )

        for field in fields(cls):
            if field.default is not MISSING:
                parser.add_argument(
                    f"--{field.name}", 
                    type=field.type, 
                    help=f"{field.name} (default: {field.default})"
                )
            else:
                parser.add_argument(
                    f"--{field.name}", 
                    type=field.type, 
                    help=f"{field.name}"
                )