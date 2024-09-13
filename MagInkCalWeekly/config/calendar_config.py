# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, asdict, fields
from MagInkCalWeekly.common import InfoBase
import json

# -----------------------------------------------------------------------------
# Calendar Config
# -----------------------------------------------------------------------------
@dataclass
class CalendarConfig(InfoBase):
    displayTZ: str
    thresholdHours: int
    maxEventsPerDay: int
    isDisplayToScreen: bool
    isShutdownOnComplete:bool
    batteryDisplayMode: int
    weekStartDay: int
    dayOfWeekText: list
    screenWidth: int
    screenHeight: int
    imageWidth: int
    imageHeight: int
    rotateAngle: int
    is24h: bool
    calendars: list

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        print("HI")
        return cls(**data)

    def to_json(self):
        return json.dumps(asdict(self))

    def print_info(self):
        print("HI")
        for field in fields(self):
            value = getattr(self, field.name)
            print(f"{field.name}: {value}")