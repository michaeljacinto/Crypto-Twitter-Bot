#!/usr/bin/env python
import sys
import json
import requests
from twython import Twython
from datetime import datetime
import schedule, time
import os.path
from spreadsheet import create_worksheet, open_spreadsheet

def main():

    # data_colleciton = []

    try:
        # data_collection = []
        data = tweet_prices()
        schedule.every(int(sys.argv[1])).minutes.do(data)


        data_collection.append(data)

        while True:
            schedule.run_pending()

    except KeyboardInterrupt:
            create_worksheet(data_collection)

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
        print(str(err))


def tweet_prices():

    with open('credentials.json') as f:
        credentials = json.load(f)

    api = Twython(credentials['apiKey'],
                  credentials['apiSecret'],
                  credentials['accessToken'],
                  credentials['accessTokenSecret'])

    user_args = sys.argv[2:]
    args = [i.upper() for i in user_args]
    coins = ','.join(args)
    now = datetime.now()
    current_datetime = now.strftime("%m/%d/%Y, %H:%M")
    cancel_tweet = True
    data = {}
    currency = 'CAD'

    try:
        r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=' + coins + '&tsyms=' + currency).json()
        tweet = ('Prices are in ' + currency + ' as of ' + str(current_datetime))
        data["current_datetime"] = current_datetime

        for index, arg in enumerate(args, 0):
            message = str(arg + ': ' + str(r[arg][currency]))
            tweet = tweet + '\n' + message
            data[arg] = r[arg][currency]

        print(data)
        return data

    # except KeyboardInterrupt as err:
    #     return data

    except KeyError as err:
        tweet = 'The ticker: ' + str(err) + ' is invalid'
        cancel_tweet = False

    except Exception as err:
        print(str(err))

    if cancel_tweet:
        api.update_status(status=tweet)


    # print(tweet)


def google_sheets_update(data):

    counter = 1

    for index, value in enumerate(data, 1):


        worksheet.update_cell(counter, idx, value)
        counter += 1
        print(value)



# def tweet_history(tweet_obj, file_name):
#
#     if os.path.isfile(file_name):
#         with open('data.json') as f:
#             data = json.load(f)
#
#         data.update(tweet_obj)
#
#         with open('data.json', 'a') as f:
#             json.dump(data, f)
#
#     else:
#         with open(file_name, 'w+') as f:
#             json.dump(tweet_obj, f)


if __name__ == "__main__":
    main()