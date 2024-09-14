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

def test_calendar_info_from_file():
    # Read directly from the file
    calendar_info = CalendarInfo.from_file("tests/data/test_cal.json") 

    # Verify the deserialized object
    assert len(calendar_info.events) == 75

    event1 = calendar_info.events[15]
    assert event1.summary == "Jorge Dad in NY"
    assert event1.startDatetime.replace(tzinfo=None) == dt.datetime(2024, 9, 13, 0, 0, 0)
    assert event1.endDatetime.replace(tzinfo=None) == dt.datetime(2024, 9, 15, 23, 59, 59, 999999)
    assert event1.isMultiday is True
    assert event1.allday is True
    assert event1.isUpdated is False
    assert event1.updatedDatetime.replace(tzinfo=None) == dt.datetime(2024, 9, 10, 13, 22, 46, 912000)

    event2 = calendar_info.events[60]
    assert event2.summary == "Drum Circle"
    assert event2.startDatetime.replace(tzinfo=None) == dt.datetime(2024, 10, 6, 10, 0)
    assert event2.endDatetime.replace(tzinfo=None) == dt.datetime(2024, 10, 6, 11, 0)
    assert event2.isMultiday is False
    assert event2.allday is False
    assert event2.isUpdated is False
    assert event2.updatedDatetime.replace(tzinfo=None) == dt.datetime(2024, 9, 1, 11, 49, 3, 890000)