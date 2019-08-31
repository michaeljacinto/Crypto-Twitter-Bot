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
        # print('Please allow access to this spreadsheet via your email, then re-run the script.')
        result = False

    return result


def create_worksheet():

    spreadsheet = open_spreadsheet()
    data = {'current_datetime': '08/30/2019, 00:10', 'ETH': 223.78, 'BTC': 12636}
    run_once = True

    if spreadsheet is False:
        print('Please allow access to this spreadsheet via your email, then re-run the script.')

    else:

        now = datetime.now()
        current_datetime = now.strftime("%m/%d/%Y, %H:%M")
        worksheet = spreadsheet.add_worksheet(title=current_datetime, rows="200", cols="20")

        values_list = worksheet.row_values(1)

        print(values_list[0] is IndexError)

        # api_time = now.strftime('%H:%M')

        counter = 1

        while run_once:
            for idx, value in enumerate(data, 1):
                worksheet.update_cell(counter, idx, value)
                counter += 1
                # worksheet.update_cell(counter, idx, data[value])
                print(value)
                run_once = False

            return worksheet


create_worksheet()

def populate_cells(data):

    worksheet = create_worksheet()
    for idx, value in enumerate(data, 1):
        worksheet.update_cell(counter, idx, value)
        counter += 1
        # worksheet.update_cell(counter, idx, data[value])
        print(value)
        # run_once = False

        return worksheet