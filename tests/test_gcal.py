# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
import sys
import pytest
import datetime as dt
import json
import logging

sys.path.append(os.path.abspath("."))
from MagInkCalWeekly.gcal import EventInfo, CalendarInfo

logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_event_info_serialization():
    event = EventInfo(
        summary="Test Event",
        startDatetime=dt.datetime(2023, 10, 1, 10, 0, 0),
        endDatetime=dt.datetime(2023, 10, 1, 12, 0, 0),
        isMultiday=False,
        allday=False,
        isUpdated=True,
        updatedDatetime=dt.datetime(2023, 10, 1, 9, 0, 0)
    )

    json_str = event.to_json()
    event_from_json = EventInfo.from_json(json_str)
    logging.basicConfig(level=logging.INFO)
    event.log_info(logging.getLogger("test_logger"))

    assert event == event_from_json

def test_calendar_info_serialization():
    event1 = EventInfo(
        summary="Test Event 1",
        startDatetime=dt.datetime(2023, 10, 1, 10, 0, 0),
        endDatetime=dt.datetime(2023, 10, 1, 12, 0, 0),
        isMultiday=False,
        allday=False,
        isUpdated=True,
        updatedDatetime=dt.datetime(2023, 10, 1, 9, 0, 0)
    )
    event2 = EventInfo(
        summary="Test Event 2",
        startDatetime=dt.datetime(2023, 10, 2, 10, 0, 0),
        endDatetime=dt.datetime(2023, 10, 2, 12, 0, 0),
        isMultiday=False,
        allday=False,
        isUpdated=True,
        updatedDatetime=dt.datetime(2023, 10, 2, 9, 0, 0)
    )

    calendar = CalendarInfo()
    calendar.events=[event1, event2]

    json_str = calendar.to_json()
    calendar_from_json = CalendarInfo.from_json(json_str)

    assert calendar.events == calendar_from_json.events

if __name__ == "__main__":
    pytest.main()