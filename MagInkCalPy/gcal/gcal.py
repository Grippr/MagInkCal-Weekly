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


class GcalHelper:
    def __init__(self, ical_url: str):
        self.logger = logging.getLogger('MagInkCalPy:GcalHelper')

#     def list_calendars(self):
#         # helps to retrieve ID for calendars within the account
#         # calendar IDs added to config.json will then be queried for retrieval of events
#         self.logger.info('Getting list of calendars')
#         calendars_result = self.service.calendarList().list().execute()
#         calendars = calendars_result.get('items', [])
#         if not calendars:
#             self.logger.info('No calendars found.')
#         for calendar in calendars:
#             summary = calendar['summary']
#             cal_id = calendar['id']
#             self.logger.info("%s\t%s" % (summary, cal_id))

    def to_datetime(self, isoDatetime, localTZ):
        # replace Z with +00:00 is a workaround until datetime library decides what to do with the Z notation
        toDatetime = dt.datetime.fromisoformat(isoDatetime.replace('Z', '+00:00'))
        return toDatetime.astimezone(localTZ)

#     def adjust_end_time(self, endTime, localTZ):
#         # check if end time is at 00:00 of next day, if so set to max time for day before
#         if endTime.hour == 0 and endTime.minute == 0 and endTime.second == 0:
#             newEndtime = localTZ.localize(
#                 dt.datetime.combine(endTime.date() - dt.timedelta(days=1), dt.datetime.max.time()))
#             return newEndtime
#         else:
#             return endTime

#     def is_multiday(self, start, end):
#         # check if event stretches across multiple days
#         return start.date() != end.date()

    def retrieve_events(self, ical_url, startDatetime, endDatetime, localTZ):
        # Get the calendar
        self.logger.info("Requesting events")
        response = requests.get(ical_url)
        print(response.content)

        # Parse the calendar
        self.logger.info("Parsing events")
        calendar = Calendar.from_ical(response.content)

        events = []
        for component in calendar.walk():
            if component.name == "VEVENT":
                event = {}
                event['summary'] = str(component.get('summary'))
                event['start'] = self.to_datetime(str(component.get('dtstart').dt), localTZ)
                event['end'] = self.to_datetime(str(component.get('dtend').dt), localTZ)
                event['description'] = str(component.get('description'))
                event['location'] = str(component.get('location'))
                event['updated'] = self.to_datetime(str(component.get('last-modified').dt), localTZ)
            even.append(event)
        return events

#         # Call the Google Calendar API and return a list of events that fall within the specified dates
#         eventList = []

#         minTimeStr = startDatetime.isoformat()
#         maxTimeStr = endDatetime.isoformat()
#         if False:
#             return eventList

#         self.logger.info('Retrieving events between ' + minTimeStr + ' and ' + maxTimeStr + '...')
#         events_result = []
#         for cal in calendars:
#             events_result.append(
#                 self.service.events().list(calendarId=cal, timeMin=minTimeStr,
#                                            timeMax=maxTimeStr, singleEvents=True,
#                                            orderBy='startTime').execute()
#             )

#         events = []
#         for eve in events_result:
#             events += eve.get('items', [])
#             # events = events_result.get('items', [])

#         if not events:
#             self.logger.info('No upcoming events found.')
#         for event in events:
#             # extracting and converting events data into a new list
#             newEvent = {}
#             newEvent['summary'] = event['summary']

#             if event['start'].get('dateTime') is None:
#                 newEvent['allday'] = True
#                 newEvent['startDatetime'] = self.to_datetime(event['start'].get('date'), localTZ)
#             else:
#                 newEvent['allday'] = False
#                 newEvent['startDatetime'] = self.to_datetime(event['start'].get('dateTime'), localTZ)

#             if event['end'].get('dateTime') is None:
#                 newEvent['endDatetime'] = self.adjust_end_time(self.to_datetime(event['end'].get('date'), localTZ),
#                                                                localTZ)
#             else:
#                 newEvent['endDatetime'] = self.adjust_end_time(self.to_datetime(event['end'].get('dateTime'), localTZ),
#                                                                localTZ)

#             newEvent['updatedDatetime'] = self.to_datetime(event['updated'], localTZ)
#             newEvent['isUpdated'] = self.is_recent_updated(newEvent['updatedDatetime'], thresholdHours)
#             newEvent['isMultiday'] = self.is_multiday(newEvent['startDatetime'], newEvent['endDatetime'])
#             eventList.append(newEvent)

#         # We need to sort eventList because the event will be sorted in "calendar order" instead of hours order
#         # TODO: improve because of double cycle for now is not much cost
#         eventList = sorted(eventList, key=lambda k: k['startDatetime'])
#         return eventList
