#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run this script first to obtain the token. Credentials.json must be in the same folder first.
To obtain Credentials.json, follow the instructions listed in the following link.
https://developers.google.com/calendar/api/quickstart/python
"""

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import sys
sys.path.append(os.path.abspath("."))
from MagInkCalPy.config import ConfigInfo

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """
    Get the configuration
    """
    config = ConfigInfo.from_file("config.json5")

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    cred_path = config.get_credential_path()
    token_path = config.get_token_path()
    print(f"Token Path: {token_path}")
    print(f"Credential Path: {cred_path}")

    if os.path.exists(token_path):
        with open(token_path) as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path) as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['start'].get('date'))
        updated = event['updated']
        print(start + " | " + end + " | " + updated + " | " + event['summary'])


if __name__ == '__main__':
    main()