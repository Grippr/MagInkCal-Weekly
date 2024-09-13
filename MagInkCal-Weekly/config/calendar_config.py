# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, asdict
from common import InfoBase
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
        return cls(**data)

    def to_json(self):
        json.dumps(asdict(self))

    def print_info(self):
        print(f"displayTZ:            {self.displayTZ}")
        print(f"thresholdHours:       {self.thresholdHours}")
        print(f"maxEventsPerDay:      {self.maxEventsPerDay}")
        print(f"isDisplayToScreen:    {self.isDisplayToScreen}")
        print(f"isShutdownOnComplete: {self.isShutdownOnComplete}")
        print(f"batteryDisplayMode:   {self.batteryDisplayMode}")
        print(f"weekStartDay:         {self.weekStartDay}")
        print(f"dayOfWeekText:        {self.dayOfWeekText}")
        print(f"screenWidth:          {self.screenWidth}")
        print(f"screenHeight:         {self.screenHeight}")
        print(f"imageWidth:           {self.imageWidth}")
        print(f"imageHeight:          {self.imageHeight}")
        print(f"rotateAngle:          {self.rotateAngle}")
        print(f"is24h:                {self.is24h}")
        print(f"calendars:            {self.calendars}")