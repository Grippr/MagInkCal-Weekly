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
from dateutil.rrule import rrulestr

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def _adjust_end_time(endTime):
    # check if end time is at 00:00 of next day, if so set to max time for day before
    if isinstance(endTime, dt.datetime):
        if endTime.time() == dt.time.min:
            tz = endTime.tzinfo
            endTime = dt.datetime.combine(endTime.date() - dt.timedelta(days=1), dt.time.max)
            endTime = endTime.replace(tzinfo=tz)
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

        if startDatetime.tzinfo is None:
            startDatetime = startDatetime.replace(tzinfo=localTZ)
        if endDatetime.tzinfo is None:
            endDatetime = endDatetime.replace(tzinfo=localTZ)

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

                rrule = component.get('rrule')
                if rrule:
                    print(event["isMultiday"], event["allday"], event["summary"])
                    rule = rrulestr(rrule.to_ical().decode('utf-8'), dtstart=start)
                    

                    for occurrence in rule.between(s_dt, e_dt, inc=True):
                        recurring_event = event.copy()
                        recurring_event['start'] = occurrence
                        recurring_event['end'] = occurrence + (end - start)
                        events.append(recurring_event)
                else:
                    # Filter events based on date range
                    if isinstance(start, dt.datetime) and isinstance(end, dt.datetime):
                        if (startDatetime <= start <= endDatetime) or (startDatetime <= end <= endDatetime):
                            events.append(event)
                    elif isinstance(start, dt.date) and isinstance(end, dt.date):
                        if (startDatetime.date() <= start <= endDatetime.date()) or (startDatetime.date() <= end <= endDatetime.date()):
                            events.append(event)
                    else:
                        self.logger.error("Event start and end times are not of the same type")
            else:
                print(component.name)
                for key in component:
                    print("      ", key, component.get(key))
        return events