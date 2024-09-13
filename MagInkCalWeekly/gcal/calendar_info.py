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
        def datetime_parser(dct):
            for key, value in dct.items():
                try:
                    dct[key] = dt.datetime.fromisoformat(value)
                except (ValueError, TypeError):
                    pass
            return dct

        data = json.loads(json_str, object_hook=datetime_parser)
        return cls(**data)

    def to_json(self):
        def datetime_serializer(obj):
            if isinstance(obj, dt.datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        return json.dumps(asdict(self), default=datetime_serializer)

    def log_info(self, logger, padding="  "):
        logger.info(f"{padding}Event starting on {self.startDatetime}:")
        max_field_length = max(len(field.name) for field in fields(self))
        for field in fields(self):
            value = getattr(self, field.name)
            logger.info(f"{padding}{padding}{field.name:<{max_field_length}}: {value}")

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
        calEndDate = calStartDate + dt.timedelta(days=(5 * 7 - 1))
        calStartDatetime = displayTZ.localize(dt.datetime.combine(calStartDate, dt.datetime.min.time()))
        calEndDatetime = displayTZ.localize(dt.datetime.combine(calEndDate, dt.datetime.max.time()))

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

        return ret

    @classmethod
    def from_json(cls, json_str):
        def datetime_parser(dct):
            for key, value in dct.items():
                try:
                    dct[key] = dt.datetime.fromisoformat(value)
                except (ValueError, TypeError):
                    pass
            return dct

        data = json.loads(json_str, object_hook=datetime_parser)
        events = [EventInfo(**event) for event in data['events']]

        ret = cls()
        ret.events = events

        return ret


    def to_json(self):
        return json.dumps({
            "events": [json.loads(event.to_json()) for event in self.events]
        })

    def log_info(self):
        for event in self.events:
            event.log_info(self.logger)

def debugthis():
    logging.basicConfig(level=logging.INFO)
    config = ConfigInfo.from_file("config.json")
    cal_info = CalendarInfo.from_config(config=config)
    cal_info.log_info()