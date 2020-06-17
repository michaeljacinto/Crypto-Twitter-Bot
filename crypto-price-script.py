#!/usr/bin/env python
import sys
import json
import requests
from twython import Twython
from datetime import datetime
import schedule
import time
import os.path
from sys import argv
from spreadsheet import create_worksheet, open_spreadsheet, populate_cells


def tweet_prices():

    with open('credentials.json') as f:
        credentials = json.load(f)

    api = Twython(credentials['Twitter']['apiKey'],
                  credentials['Twitter']['apiSecret'],
                  credentials['Twitter']['accessToken'],
                  credentials['Twitter']['accessTokenSecret'])

    user_args = sys.argv[2:]
    args = [i.upper() for i in user_args]
    coins = ','.join(args)
    now = datetime.now()
    current_datetime = now.strftime("%m/%d/%Y, %H:%M")
    current_time = now.strftime("%H:%M")
    # cancel_tweet = True
    data = {}
    currency = 'CAD'

    try:
        r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=' +
                         coins + '&tsyms=' + currency).json()
        tweet = ('Prices are in ' + currency +
                 ' as of ' + str(current_datetime))
        data["current_time"] = current_time

        for index, arg in enumerate(args, 0):
            message = str(arg + ': ' + str(r[arg][currency]))
            tweet = tweet + '\n' + message
            data[arg] = r[arg][currency]

        # populate_cells(data)
        api.update_status(status=tweet)
        print(tweet)
        print(data)
        return data

    except KeyError as err:
        tweet = 'The ticker: ' + str(err) + ' is invalid'
        cancel_tweet = False

    except Exception as err:
        print(str(err))


# def google_sheets_update(data):

#     counter = 1

#     for index, value in enumerate(data, 1):

#         worksheet.update_cell(counter, idx, value)
#         counter += 1
#         print(value)

def main():

    try:
        # tweet_prices()
        # user_minutes = int(sys.argv[1])
        schedule.every(int(sys.argv[1])).minutes.do(tweet_prices)
    # try:
    #     print("hello")
    #     # schedule.every(0.5).minutes.do(tweet_prices)
    #     # schedule.every(float(sys.argv[1])).minutes.do(tweet_prices)

    #     tweet_prices()

        while True:

            # Checks whether a scheduled task
            # is pending to run or not
            schedule.run_pending()
            time.sleep(1)

    except Exception as err:

        print()
        print('Usage: python crypto-price-script <min> <coin> <coin>*')
        print('<min>: required, must be a number')
        print('<coin>: required, valid coin ticker e.g. BTC ETH')
        print('<coin>* may use more than 1 coin')
        print()
        print('e.g. python crypto-price-script 5 BTC ETH')
        print('This will tweet the price of BTC and ETH every 5 minutes to:'
              ' https://twitter.com/script_crypto')
        print('hahsahsa' + str(err))


if __name__ == "__main__":
    main()
