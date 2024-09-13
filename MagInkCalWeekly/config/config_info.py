# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, fields, asdict
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

    def to_json(self):
        return json.dumps(asdict(self))

    def print_info(self):
        for field in fields(self):
            value = getattr(self, field.name)
            print(f"{field.name}: {value}")