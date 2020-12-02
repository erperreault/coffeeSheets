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

def stripBufferZero(str):
    if str[-2] == '0':
        return (str[:-2] + str[-1])
    else:
        return str

# this is a change

TODAY = stripBufferZero( datetime.date.today().strftime('%B %d') )

TOMORROW = stripBufferZero( (datetime.date.today() + datetime.timedelta(days=1))
    .strftime('%B %d') )

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

# Snag a copy of the spreadsheet.
coffeeSheetsTesterCopy = service.spreadsheets().get(spreadsheetId=coffeeSheetsTesterID, includeGridData=True).execute()

def getAllTabs(spreadsheet):
    # Get tab IDs
    # args: main spreadsheet (object)
    # returns: ['title', 'title', 'title']
    return [sheet['properties']['title'] for sheet in spreadsheet['sheets']]

def getTabID(spreadsheet, index):
    # args: main spreadsheet ID (str)
    # returns: 'template ID'
    return spreadsheet['sheets'][index]['properties']['sheetId']

def getLastPR(sheetID, index):
    # Get last batch number.
    # args: main spreadsheet ID (str), index (int)
    # returns: batch number (int)
    lastSheet = "'" + getAllTabs(coffeeSheetsTesterCopy)[index] + "'!B:B"
    pr = service.spreadsheets().values().get(spreadsheetId=sheetID, range=lastSheet).execute()
    result = int(pr['values'][-1][0]) + 1
    return str(result)

def newFromTemplate(sheetID, name):
    # Create new worksheet for TODAY's date, if it doesn't exist already. 
    # Fill from template.
    try:
        service.spreadsheets().batchUpdate(spreadsheetId=sheetID, body={
            'requests':[{
                'duplicateSheet': {
                    'sourceSheetId': getTabID(coffeeSheetsTesterCopy, 0),
                    'insertSheetIndex': 1,
                    'newSheetName': name
                }
            }]
        }).execute()
        print('New tab created.')
    except:
        print('New tab not created.')
        
def updatePR(sheetID, index):
    # Update current tab to start from the next PR based on previous tab. 
    try:
        service.spreadsheets().values().update(
            spreadsheetId=sheetID, 
            range="'" + getAllTabs(coffeeSheetsTesterCopy)[index] + "'!B2",
            valueInputOption='RAW',
            body={ 
                'range': ("'" + getAllTabs(coffeeSheetsTesterCopy)[index] + "'!B2"),
                'values': [ [getLastPR(coffeeSheetsTesterID, index+1)] ] 
            }
        ).execute()
        print(f'Starting from PR#{getLastPR(coffeeSheetsTesterID, index+1)}.')
    except Exception as x:
        print(str(x))

def testSuite():
    newFromTemplate(coffeeSheetsTesterID, TODAY)
    updatePR(coffeeSheetsTesterID, 1)
    newFromTemplate(coffeeSheetsTesterID, TOMORROW)

#TODO Get needed amounts from readShopify.

#TODO Send roast schedule to Cropster.

#TODO Make a GUI for the thing.

#TODO Bundle it and throw it on GitHub.

#TODO Make universal / executable / log-in-able ?

####################################################################################

# testSuite()