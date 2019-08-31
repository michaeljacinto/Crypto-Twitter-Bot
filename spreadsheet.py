import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime
import json


def open_spreadsheet():

    with open('credentials.json') as f:
        credentials = json.load(f)

    email = credentials['email']
    spreadsheet_name = credentials['spreadsheet_name']

    try:
        scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open(spreadsheet_name)
        result = spreadsheet
        print(spreadsheet)

    except Exception:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        spreadsheet = client.create(spreadsheet_name)
        spreadsheet.share(email, perm_type='user', role='writer')
        result = False

    return result


def create_worksheet(data):

    spreadsheet = open_spreadsheet()
    run_once = True

    if spreadsheet is False:
        print('Please allow access to this spreadsheet via your email, then re-run the script.')

    else:

        now = datetime.now()
        current_datetime = now.strftime("%m/%d/%Y")

        try:
            worksheet = spreadsheet.add_worksheet(title=current_datetime, rows="200", cols="20")

            counter = 1

            while run_once:
                for idx, value in enumerate(data, 1):
                    worksheet.update_cell(counter, idx, value)
                    print(value)
                    run_once = False

        except Exception:
            worksheet = spreadsheet.worksheet(current_datetime)

        return worksheet


def populate_cells(data):

    counter = 2
    worksheet = create_worksheet(data)
    values = worksheet.row_values(counter)

    while values:
        counter += 1
        values = worksheet.row_values(counter)

    for idx, value in enumerate(data, 1):
        worksheet.update_cell(counter, idx, data[value])

        print(value)

    return worksheet