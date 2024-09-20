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
@pytest.fixture
def calendar_info():
    calendar_info = CalendarInfo()
    calendar_info.events = [
        EventInfo(
            summary="Event 1",
            startDatetime=dt.datetime(2023, 10, 1, 10, 0),
            endDatetime=dt.datetime(2023, 10, 1, 12, 0),
            isMultiday=False,
            allday=False,
            isUpdated=False,
            updatedDatetime=dt.datetime(2023, 10, 1, 9, 0)
        ),
        EventInfo(
            summary="Event 2",
            startDatetime=dt.datetime(2023, 10, 2, 14, 0),
            endDatetime=dt.datetime(2023, 10, 2, 16, 0),
            isMultiday=False,
            allday=False,
            isUpdated=False,
            updatedDatetime=dt.datetime(2023, 10, 2, 13, 0)
        ),
        EventInfo(
            summary="Event 3",
            startDatetime=dt.datetime(2023, 10, 1, 18, 0),
            endDatetime=dt.datetime(2023, 10, 1, 20, 0),
            isMultiday=False,
            allday=False,
            isUpdated=False,
            updatedDatetime=dt.datetime(2023, 10, 1, 17, 0)
        )
    ]
    calendar_info.currDate = dt.date(2023, 10, 1) 
    calendar_info.startDate = dt.date(2023, 10, 1)
    calendar_info.endDate = dt.date(2023, 10, 7)

    return calendar_info

def test_get_events_from_date_single_event(calendar_info):
    date = dt.date(2023, 10, 2)
    events = calendar_info.get_events_from_date(date)
    assert len(events) == 1
    assert events[0].summary == "Event 2"

def test_get_events_from_date_multiple_events(calendar_info):
    date = dt.date(2023, 10, 1)
    events = calendar_info.get_events_from_date(date)
    assert len(events) == 2
    assert events[0].summary == "Event 1"
    assert events[1].summary == "Event 3"

def test_get_events_from_date_no_events(calendar_info):
    date = dt.date(2023, 10, 3)
    events = calendar_info.get_events_from_date(date)
    assert len(events) == 0

def test_to_json(calendar_info):
    json_str = calendar_info.to_json()
    assert '"summary": "Event 1"' in json_str
    assert '"summary": "Event 2"' in json_str
    assert '"summary": "Event 3"' in json_str

def test_from_json(calendar_info):
    json_str = calendar_info.to_json()
    new_calendar_info = CalendarInfo.from_json(json_str)
    assert len(new_calendar_info.events) == 3
    assert new_calendar_info.events[0].summary == "Event 1"
    assert new_calendar_info.events[1].summary == "Event 2"
    assert new_calendar_info.events[2].summary == "Event 3"

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
    calendar.currDate = dt.date(2023, 10, 1)
    calendar.startDate = dt.date(2023, 10, 1)
    calendar.endDate = dt.date(2023, 10, 7)

    json_str = calendar.to_json()
    calendar_from_json = CalendarInfo.from_json(json_str)

    assert calendar.events == calendar_from_json.events
    assert calendar.currDate == calendar_from_json.currDate

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

    assert calendar_info.currDate == dt.date(2024, 9, 15)

import pytest
import datetime as dt
from MagInkCalWeekly.gcal.calendar_info import CalendarInfo, EventInfo