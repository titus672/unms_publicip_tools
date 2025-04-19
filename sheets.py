#!/usr/bin/env python

from config import CONFIG
import os.path
from misc_tools import pprint, index_to_column
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheet:
    def __init__(self):
        self.config = CONFIG()
        self.spreadsheet_id = self.config.spreadsheet_id
        self.range = self.config.range
        self.page = self.config.page
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)
            self.sheet = service.spreadsheets()
            result = (
                self.sheet.values()
                .get(spreadsheetId=self.spreadsheet_id, range=self.range)
                .execute()
            )

        except HttpError as err:
            print(err)

    def get_range(self, range):
        result = self.sheet.values().get(
            spreadsheetId=self.spreadsheet_id, range=range).execute()
        values = result.get("values", [])
        return values

    def update_range(self, range, value):
        body = {
            'values': [[value]]
        }
        result = self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range,
            valueInputOption='RAW',
            body=body
        ).execute()

        # print(f"{result.get('updatedCells')} cells updated.")

    def clear_ranges(self):
        clear_request = {
            'ranges': self.config.range_to_clear
        }
        self.sheet.values().batchClear(
            spreadsheetId=self.spreadsheet_id,
            body=clear_request
        ).execute()


# 2 parameters, sheet takes the  values from the sheet, and the value parameter
# is the value you want to find in the sheet. returns the coordinates of the
# first match


def find_value_in_sheet(sheet, value):
    values = sheet
    # start row value at 2 because we aren't reading the first row from the sheet
    row = 2
    for v in values:
        # the column index is offset so that it returns the column for the description
        column = 1
        for a in v:

            if a == value:

                # returns the coordinates of the match
                return f"{index_to_column(column)}{row}"
            column += 1
        row += 1


def main():
    sheet = Sheet()
    values = sheet.get_range(sheet.range)


if __name__ == "__main__":
    main()
