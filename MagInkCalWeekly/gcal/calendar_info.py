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
        # TODO: Fix implement this
        pass

    def log_info(self, logger, padding="  "):
        logger.info(f"{padding}Event starting on {self.startDatetime}:")
        for field in fields(self):
            value = getattr(self, field.name)
            logger.info(f"{padding}{padding}{field.name}: {value}")


# -----------------------------------------------------------------------------
# Calendar Info
# -----------------------------------------------------------------------------
class CalendarInfo(InfoBase):
    def __init__(
        self,
        cred_path,
        token_path, 
    ):
        self.gcalHelper = GcalHelper(
            cred_path=cred_path,
            token_path=token_path,
        )
        self.logger = logging.getLogger("CalendarInfo")
        self.events = []

    @classmethod
    def from_config(cls, config: ConfigInfo):
        ret = CalendarInfo(
            cred_path=config.get_credential_path(),
            token_path=config.get_token_path(),
        )
        calendars = config.calendars

        displayTZ = config.get_tz()
        currDatetime = dt.datetime.now(displayTZ)
        ret.logger.info("Time synchronised to {}".format(currDatetime))

        currDate = currDatetime.date()
        calStartDate = currDate - dt.timedelta(days=((currDate.weekday() + (7 - config.weekStartDay)) % 7))
        calEndDate = calStartDate + dt.timedelta(days=(5 * 7 - 1))
        calStartDatetime = displayTZ.localize(dt.datetime.combine(calStartDate, dt.datetime.min.time()))
        calEndDatetime = displayTZ.localize(dt.datetime.combine(calEndDate, dt.datetime.max.time()))

        ret.logger.debug(f"currDate: {currDate}")
        ret.logger.debug(f"calStartDate: {calStartDate}")
        ret.logger.debug(f"calEndDate: {calEndDate}")
        ret.logger.debug(f"calStartDatetime: {calStartDatetime}")
        ret.logger.debug(f"calEndDatetime: {calEndDatetime}")

        eventList = ret.gcalHelper.retrieve_events(
            calendars, 
            calStartDatetime, 
            calEndDatetime, 
            displayTZ, 
            config.thresholdHours
        )

        for event_dict in eventList:
            event = EventInfo(**event_dict)
            ret.events.append(event)

        return ret

    @classmethod
    def from_json(cls, json_str):
        pass

    def to_json(self):
        return json.dumps(self)

    def log_info(self):
        pass

def debugthis():
    logging.basicConfig(level=logging.INFO)
    config = ConfigInfo.from_file("config.json")
    CalendarInfo.from_config(config=config)

    # gcalHelper = GcalHelper()
    # print("HI")
    # print(gcalHelper.list_calendars())
    # #print(gcalHelper.retrieve_events(calendars, startDatetime, endDatetime, localTZ, thresholdHours))