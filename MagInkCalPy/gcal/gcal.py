#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is where we retrieve events from the Google Calendar. Before doing so, make sure you have both the
credentials.json and token.pickle in the same folder as this file. If not, run quickstart.py first.
"""

# from __future__ import print_function
import datetime as dt
# import pickle
# import os.path
# import pathlib
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

import logging
import requests
from icalendar import Calendar
from MagInkCalPy.config.config_info import ConfigInfo

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def _adjust_end_time(endTime):
    # check if end time is at 00:00 of next day, if so set to max time for day before
    if isinstance(endTime, dt.datetime):
        if endTime.time() == dt.time.min:
            endTime = dt.datetime.combine(endTime.date() - dt.timedelta(days=1), dt.time.max)
    else: 
        # It's a dateime.date object, meaning it's an all-day event. 
        # In ICS, the end date is exclusive, meaning the end day is actually the
        # day after the event ends, so we need to subtract a day for our
        # purposes
        endTime = endTime - dt.timedelta(days=1)
    return endTime


def _is_multiday(start, end):
    # check if event stretches across multiple days
    if isinstance(start, dt.datetime) and isinstance(end, dt.datetime):
        return start.date() != end.date()
    else: # It's a dateime.date object
        return start != end


class GcalHelper:
    def __init__(self, ical_url: str):
        self.logger = logging.getLogger('MagInkCalPy:GcalHelper')

    def retrieve_events(self, ical_url, startDatetime, endDatetime, localTZ):
        # Get the calendar
        self.logger.info("Requesting events")
        response = requests.get(ical_url)

        # Parse the calendar
        self.logger.info("Parsing events")
        calendar = Calendar.from_ical(response.content)

        events = []
        for component in calendar.walk():
            if component.name in ("VALARM", "VTIMEZONE", "VCALENDAR", "DAYLIGHT", "STANDARD"):
                continue
            elif component.name == "VEVENT":
                event = {}
                start = component.get('dtstart').dt
                end = component.get('dtend').dt if component.get("dtend") else start

                # Adjust to local timezone
                allday = not isinstance(start, dt.datetime)
                if not allday:
                    start = start.astimezone(localTZ)
                    end = end.astimezone(localTZ)
                
                # Adjust end time if necessary
                end = _adjust_end_time(end)
    
                event['summary'] = str(component.get('summary'))
                event['start'] = start
                event['end'] = end
                event['isMultiday'] = _is_multiday(start, end)
                event['allday'] = allday
                events.append(event)
            else:
                print(component.name)
                for key in component:
                    print("      ", key, component.get(key))
        return events