#!Python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

TODAY = datetime.date.today().strftime('%B %d')
TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
TOMORROW = TOMORROW.strftime('%B %d')
if TOMORROW[-2] == '0':
    TOMORROW = TOMORROW[:-2] + TOMORROW[-1]

def main(): 
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Tester
    coffeeSheetsTesterID = '1Bx9OF2hMm_M1AjKCdJwq8DCgWxeCu7hk6VURbArNEjA'

    # Copy of production sheet (SP account)
    # coffeeSheetsTesterID = '1XoQ9uyz_fUBmvowLoOO2dvoniOeZiq6x0AEH9v88Xgg'

    