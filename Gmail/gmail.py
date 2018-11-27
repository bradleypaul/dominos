from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
from base64 import b64decode
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def list_messages(service, user_id, label_ids=[]):
    try:
        response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except errors.HttpError:
        print('An error occurred')

def get_message_body(message):
    body = message['payload']['body']['data']
    return b64decode(body).decode('utf-8')

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return get_message_body(message)
    except errors.HttpError:
        print('An error occurred')

def get_latest_message(service, user_id, label_ids=[]):
    message = list_messages(service, user_id, label_ids)[0]
    return get_message(service, 'me', message['id'])

def get_path(filename): 
    return os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), filename)

def get_email():    
    store = file.Storage(get_path('token.json'))
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(get_path('credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # label id already found for 'Dominos'
    label_ids = ['Label_4688577403933683502']

    return get_latest_message(service, 'me', label_ids)

def main():
    print(get_email())

if __name__ == '__main__':
    main()    