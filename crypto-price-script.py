#!/usr/bin/env python
import sys
import json
import requests
from twython import Twython
from datetime import datetime
import schedule, time
import os.path


def main():

    try:
        schedule.every(int(sys.argv[1])).minutes.do(tweet_prices)

        while True:
            schedule.run_pending()

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
    cancel_tweet = False
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

        tweet_history(data, 'data.json')

        print(data)

    except KeyError as err:
        tweet = 'The ticker: ' + str(err) + ' is invalid'
        cancel_tweet = True

    except Exception as err:
        print(str(err))

    if not cancel_tweet:
        api.update_status(status=tweet)

    print(tweet)


def tweet_history(tweet_obj, file_name):

    if os.path.isfile(file_name):
        with open('data.json') as f:
            data = json.load(f)

        data.update(tweet_obj)

        with open('data.json', 'a') as f:
            json.dump(data, f)

    else:
        with open(file_name, 'w+') as f:
            json.dump(tweet_obj, f)


if __name__ == "__main__":
    main()