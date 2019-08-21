#!/usr/bin/env python
import sys
import json
import requests
from twython import Twython
from datetime import datetime
import schedule, time


def main():

    try:
        schedule.every(int(sys.argv[1])).minutes.do(tweet_prices)

        while True:
            schedule.run_pending()

    except:
        print()
        print('Usage: python crypto-price-script <min> <coin> <coin>*')
        print('<min>: required, must be a number')
        print('<coin>: required, valid coin ticker e.g. BTC ETH')
        print('<coin>* may use more than 1 coin')
        print()
        print('e.g. python crypto-price-script 5 BTC ETH')
        print('This will tweet the price of BTC and ETH every 5 minutes to:'
              ' https://twitter.com/script_crypto')


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

    try:
        r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=' + coins + '&tsyms=CAD').json()
        tweet = ('Prices are in CAD as of ' + str(current_datetime))

        for index, arg in enumerate(args, 0):
            message = str(arg + ': ' + str(r[arg]['CAD']))
            tweet = tweet + '\n' + message

    except KeyError as err:
        tweet = 'The ticker: ' + str(err) + ' is invalid'
        cancel_tweet = True

    if not cancel_tweet:
        api.update_status(status=tweet)

    print(tweet)


if __name__ == "__main__":
    main()