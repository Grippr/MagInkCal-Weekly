# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, asdict, fields
import datetime as dt
import json
import logging

from MagInkCalWeekly.common import InfoBase
from MagInkCalWeekly.config import ConfigInfo
from .gcal import GcalHelper

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
def _datetime_serializer(obj):
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    elif isinstance(obj, dt.date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def _datetime_parser(dct):
    for key, value in dct.items():
        try:
            if key=="currDate" or key=="startDate" or key=="endDate":
                dct[key] = dt.date.fromisoformat(value)
            else:
                dct[key] = dt.datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return dct

# -----------------------------------------------------------------------------
# Event Info
# -----------------------------------------------------------------------------
@dataclass
class EventInfo(dict, InfoBase):
    summary: str
    startDatetime: dt.datetime
    endDatetime: dt.datetime
    isMultiday: bool
    allday: bool
    isUpdated: bool
    updatedDatetime: dt.datetime

    @classmethod
    def from_json(cls, json_str):


        data = json.loads(json_str, object_hook=_datetime_parser)
        return cls(**data)

    def to_json(self):
        return json.dumps(asdict(self), default=_datetime_serializer)

    def log_info(self, logger, padding="  "):
        logger.info(f"{padding}Event starting on {self.startDatetime}:")
        max_field_length = max(len(field.name) for field in fields(self))
        for field in fields(self):
            value = getattr(self, field.name)
            logger.info(f"{padding}{padding}{field.name:<{max_field_length}}: {value}")

    def get_cal_str(self, max_width):
        ret = ""
        if self.isMultiday:
            ret += ">"

        if self.allday:
            ret += f"{self.summary}"
        else:
            time_str = self.startDatetime.strftime("%H:%M").lstrip("0")
            ret += f"{time_str} {self.summary}"

        if len(ret) > max_width:
            ret = ret[:max_width-3] + "..."
        return ret



# -----------------------------------------------------------------------------
# Calendar Info
# -----------------------------------------------------------------------------
class CalendarInfo(InfoBase):
    def __init__(
        self,
    ):
        self.logger = logging.getLogger("CalendarInfo")
        self.events = []

    @classmethod
    def from_config(cls, config: ConfigInfo):
        #Initialize the calendar
        ret = CalendarInfo()

        # Grab some information from the config
        calendars = config.calendars

        displayTZ = config.get_tz()
        currDatetime = dt.datetime.now(displayTZ)
        ret.logger.info("Time synchronised to {}".format(currDatetime))

        currDate = currDatetime.date()
        calStartDate = currDate - dt.timedelta(days=((currDate.weekday() + (7 - config.weekStartDay)) % 7))
        calEndDate = calStartDate + dt.timedelta(days=(config.numWeeks * 7 - 1))
        calStartDatetime = displayTZ.localize(dt.datetime.combine(calStartDate, dt.datetime.min.time()))
        calEndDatetime = displayTZ.localize(dt.datetime.combine(calEndDate, dt.datetime.max.time()))

        assert calStartDate.weekday() == config.weekStartDay, f"Week start day ({config.weekStartDay}) does not match the start date ({calStartDate.weekday()})"

        cred_path=config.get_credential_path()
        token_path=config.get_token_path()

        ret.logger.debug(f"currDate: {currDate}")
        ret.logger.debug(f"calStartDate: {calStartDate}")
        ret.logger.debug(f"calEndDate: {calEndDate}")
        ret.logger.debug(f"calStartDatetime: {calStartDatetime}")
        ret.logger.debug(f"calEndDatetime: {calEndDatetime}")
        ret.logger.debug(f"calEndDatetime: {cred_path}")
        ret.logger.debug(f"calEndDatetime: {token_path}")

        # Set up the gcalHelper
        gcalHelper = GcalHelper(
            cred_path=cred_path,
            token_path=token_path,
        )

        # Get the events
        eventList = gcalHelper.retrieve_events(
            calendars, 
            calStartDatetime, 
            calEndDatetime, 
            displayTZ, 
            config.thresholdHours
        )

        # Save the events
        for event_dict in eventList:
            event = EventInfo(**event_dict)
            ret.events.append(event)
        ret.currDate = currDate
        ret.startDate = calStartDate
        ret.endDate = calEndDate

        return ret

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str, object_hook=_datetime_parser)
        events = [EventInfo(**event) for event in data['events']]

        ret = cls()
        ret.events = events

        ret.currDate      = data['currDate']
        ret.startDate = data['startDate']
        ret.endDate   = data['endDate']

        return ret

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as file:
            json_str = file.read()
        return cls.from_json(json_str)

    def to_json(self):
        return json.dumps({
            "events": [json.loads(event.to_json()) for event in self.events],
            "startDate": _datetime_serializer(self.startDate),
            "endDate": _datetime_serializer(self.endDate),
            "currDate": _datetime_serializer(self.currDate)
        })

    def to_file(self, filename):
        json_str = self.to_json()
        with open(filename, "w") as file:
            file.write(json.dumps(json.loads(json_str), indent=4))

    def log_info(self, full=False):
        self.logger.info("Calendar Info:")
        self.logger.info(f"    Current day: {self.currDate}")
        self.logger.info(f"    Cal Start Dat: {self.startDate}")
        self.logger.info(f"    Cal End Date: {self.endDate}")
        self.logger.info(f"    Num Events:{len(self.events)}")
        if full:
            for event in self.events:
                event.log_info(self.logger)
    
    def get_events_from_date(self, date):
        return [event for event in self.events if event.startDatetime.date() == date]
    

def debug_this():
    logging.basicConfig(level=logging.INFO)
    config = ConfigInfo.from_file("config.json5")
    cal_info = CalendarInfo.from_config(config=config)
    cal_info.log_info()
    print(cal_info.to_json())