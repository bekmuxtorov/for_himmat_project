from __future__ import print_function
from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from data.config import SPREADSHEET_ID

# Spreadsheet id

# Sheet Name and Range to Read
WRITE_RANGE = "Users!A1:G3000"

# The boundary of script
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


# Configuration for python to sheet link
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES)
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)


async def write_range(value: list) -> bool:
    spreadsheet_id = SPREADSHEET_ID
    range_name = WRITE_RANGE
    value_input_option = 'USER_ENTERED'
    body = {
        'values': [value,]
    }
    try:
        spreadsheet_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        return True
    except Exception as e:
        print(''.join(['='*20, "google sheet write_range"], '='*20))
        print(e)
        return False
