#!Python3

from __future__ import print_function
import datetime, setup
from pprint import pprint
from setup import sheet

def stripBufferZero(str):
    """Clean up date format from datetime to match Sheets format."""
    if str[-2] == '0':
        return (str[:-2] + str[-1])
    else:
        return str

TODAY = stripBufferZero( datetime.date.today().strftime('%B %d') )
TOMORROW = stripBufferZero( (datetime.date.today() + datetime.timedelta(days=1)).strftime('%B %d') )

def getTabNames(ID):
    return [sheet['properties']['title'] for sheet in sheet.get(spreadsheetId=ID).execute()['sheets']]

def getTabIDs(ID):
    return [sheet['properties']['sheetId'] for sheet in sheet.get(spreadsheetId=ID).execute()['sheets']]

def readCells(ID, cells):
    result = sheet.values().get(spreadsheetId=ID, range=cells).execute()
    return [entry[0] for entry in result['values']]

def getRoastNumbers(ID):
    coffeeNames = readCells(ID, f'{getTabNames(ID)[1]}!A3:A29')
    batchNumbers = readCells(ID, f'{getTabNames(ID)[1]}!I3:I29')
    yayDict = dict(zip(coffeeNames, batchNumbers))
    return yayDict

def getLastPR(ID, index):
    prs = readCells(ID, f'{getTabNames(ID)[index+1]}!B1:B')
    result = int(prs[-1])
    return result

def newFromTemplate(ID, name):
    """Make a new blank tab to fill."""
    sheet.batchUpdate(
        spreadsheetId=ID, 
        body={
            'requests':[{
                'duplicateSheet': {
                    'sourceSheetId': getTabIDs(ID)[0],
                    'insertSheetIndex': 1,
                    'newSheetName': name
                }
            }]
        }).execute()

def continueFromLastPR(ID, index):
    sheet.values().update(
            spreadsheetId=ID, 
            range=f"{getTabNames(ID)[index]}!B2:B2",
            valueInputOption='RAW',
            body={ 
                'range': (f"{getTabNames(ID)[index]}!B2:B2"),
                'values': [ [(int(getLastPR(ID, index)) + 1)] ] 
            }
        ).execute()

def getLogCoffees(ID):
    result = {}
    step = 16
    for coffee in readCells(ID, f'{getTabNames(ID)[1]}!F16:F44'):
        result[coffee] = f'{getTabNames(ID)[1]}!F{step}:F{step}'
        step += 1
    return result

def populateBatches(ID, index, numbers):
    logCoffees = getLogCoffees(ID)
    step = 2
    target = f'{getTabNames(ID)[index]}!C'
    for coffee in numbers.keys():
        if coffee in logCoffees.keys():
            print(coffee)
            for i in range(int(numbers[coffee])):
                sheet.batchUpdate(
                    spreadsheetId=ID,
                    body={
                        'requests':[{
                            'copyPaste': {
                                'source': dict.fromkeys({ logCoffees[coffee] }),
                                'destination': dict.fromkeys({ f'{target}{step}:C{step}' }),
                                'pasteType': 'PASTE_NORMAL',
                                'pasteOrientation': 'NORMAL'
                            }
                        }]
                    }
                ).execute()
                step += 1
        else:
            print(f'Error: {coffee} not in Roast Logs template.')

def makeRoastTabs(ID, numbers):
    """Called in main.py
    Create new tabs for today and tomorrow, populate today with roast math.
    """
    newFromTemplate(ID, TODAY)
    continueFromLastPR(ID, 1)
    newFromTemplate(ID, TOMORROW)
    populateBatches(ID, 2, numbers)