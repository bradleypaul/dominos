from __future__ import print_function
import datetime
import googleapiclient.discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'


def get_path(filename):
    return os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), filename)

def create_event(start_time, end_time):
    return {
        'summary': 'Domino\'s',
        'location': 'Western Trail, Georgetown, TX',
        'description': 'work',
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Chicago',
        },
        'attendees': [
            {'email': 'bradleypauld@gmail.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 30 * 60},
                {'method': 'popup', 'minutes': 120},
            ],
        },
    }

def add(times):
    store = file.Storage(get_path('token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            get_path('credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API for all times
    for time in times:
        event = create_event(time['start'], time['end'])
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event Created:')