from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '11QxgM2EySs3vbZkxoKJfbLUo7ccfD-fAC06-raQ9gQ8'
RANGE_NAME = 'Base Statistics!B3:C10'


class SheetsAPIController:

    def __init__(self):
        self.credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:

            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/luke/workspace/T-PLE/scripts/apiController/credentials.json', SCOPES)
                self.credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

        self.service = build('sheets', 'v4', credentials=self.credentials)

    @staticmethod
    def queryAndValidate(sheet, spreadsheetID, sheetRange):
        queryResults = sheet.values().get(
            spreadsheetId=spreadsheetID,
            range=sheetRange).execute()

        queryValues = queryResults.get('values', [])

        if not queryValues:
            print("No values found in range provided ({0}). Exiting".format(sheetRange))
            sys.exit()

        else:
            return queryValues

    @staticmethod
    def sendWrite(sheet, values, spreadsheetID, sheetRange, valueInputOption):

        body = {
            'values': values
        }

        sheet.values().update(
            spreadsheetId=spreadsheetID, range=sheetRange,
            valueInputOption=valueInputOption, body=body).execute()
