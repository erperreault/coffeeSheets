#!Python3

from __future__ import print_function
from googleapiclient.discovery import build
from pprint import pprint
from setup import sheet
from sheetsFunctions import getRoastNumbers, makeRoastTabs, readCells, getTabNames, getLogCoffees, populateBatches

roastCalcID = '1h2BnGxmtncik8zc361Fp1sroB8eLp8Rh7RE9H0K3Lg0'
roastLogID = '1_jW0YLphQxGyPNow-r3PMDhrGiNNKwBRbLxMPYP4sFo'

def testSuite(x):
    numbers = getRoastNumbers(roastCalcID)
    if x == 1:
        pprint(numbers)
    elif x == 2:
        pprint(makeRoastTabs(roastLogID, numbers))
    elif x == 3:
        pprint(readCells(roastLogID, f'{getTabNames(roastLogID)[0]}!F16:F43'))

populateBatches(roastLogID, 1, getRoastNumbers(roastCalcID))

# Make tabs in roastLog with correct dates
# Make dict of active coffee names and their template addresses ('Decaf [25]':'Template!F16')
#TODO Fill tabs in roastLog with batches
#TODO Get needed amounts from readShopify.
#TODO Send roast schedule to Cropster.
#TODO Make a GUI for the thing.
#TODO Bundle it and throw it on GitHub.
#TODO Make universal / executable / log-in-able ?