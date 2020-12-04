#!Python3

from __future__ import print_function
import pickle, os.path, datetime, base64, requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from writeSheets import *
from b64 import b64creds

auth = 'Basic ' + b64creds
print(auth)
contentType = 'application/vnd.api+json; charset=utf-8'
userAgent = 'coffeeSheetsTest-SP'
headers = {'Authorization':auth, 'Content-Type':contentType, 'User-Agent':userAgent}

r = requests.get('https://c-sar.cropster.com/api/v2/users/AdXV', params=headers)
print(r.url)

def getWeights(index):
    # Reference spreadsheet for actual yield weights.
    # args: index of desired spreadsheet (int)
    # returns: {'pr':'weight', 'pr':'weight', ...}
    prRange = "'" + getAllTabs(coffeeSheetsTesterCopy)[index] + "'!B2:B"
    weightRange = "'" + getAllTabs(coffeeSheetsTesterCopy)[index] + "'!D2:D"

    weights = [weight[0] for weight in service.spreadsheets().values().get(
        spreadsheetId=coffeeSheetsTesterID, range=weightRange).execute()['values']]
    prs = [pr[0] for pr in service.spreadsheets().values().get(
        spreadsheetId=coffeeSheetsTesterID, range=prRange).execute()['values']]

    return dict(zip(prs, weights))



#TODO Send roasted weights to Cropster at end of day.
    #TODO Check Cropster to see which batches need their yield weights.
    #TODO Update Croster batches with appropriate yield weights.