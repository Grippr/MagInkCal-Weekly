# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from argparse import ArgumentParser
from dataclasses import dataclass, fields, asdict, MISSING
import logging
import json5 as json # json5 is a superset of JSON that allows comments
import os
from pytz import timezone
from pathlib import Path

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
    numWeeks: int
    icalUrl: str
    calendarImagePath: str = None

    
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
        logger = logging.getLogger("MagInkCalPy:ConfigInfo")
        for field in fields(self):
            value = getattr(self, field.name)
            logger.info(f"{field.name}: {value}")
    
    # CalendarInfo Utilities
    def get_ical_url_file_path(self):
        return Path(self.privateDirectory) / self.icalUrl

    def get_ical_url(self):
        with open(self.get_ical_url_file_path()) as fp:
            return fp.read().strip()

    def get_tz(self):
        return timezone(self.displayTZ)
   
    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
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
                )