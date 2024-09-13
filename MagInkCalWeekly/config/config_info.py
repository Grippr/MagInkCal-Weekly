# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, fields, asdict
import logging

from MagInkCalWeekly.common import InfoBase
import json

# -----------------------------------------------------------------------------
# Calendar Config
# -----------------------------------------------------------------------------
@dataclass
class ConfigInfo(InfoBase):
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
    privateDirectory: str
    credentialsFileName: str
    tokenFileName: str
    logger = logging.getLogger("CalendarConfig")
    

    def to_json(self):
        return json.dumps(asdict(self))

    def log_info(self):
        for field in fields(self):
            value = getattr(self, field.name)
            self.logger.info(f"{field.name}: {value}")