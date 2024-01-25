from __future__ import print_function
from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from data.config import SPREADSHEET_ID

# Spreadsheet id

# Sheet Name and Range to Read
READ_RANGE = "Suhbatlar!A1:B5"

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


async def read_range():
    range_name = READ_RANGE
    spreadsheet_id = SPREADSHEET_ID
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows


async def get_talks_dict():
    results = await read_range()
    results_dict = {}
    for item in results[1:]:
        results_dict[item[0]] = item[1].split(',')
    return results_dict
