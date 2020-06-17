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
from twilio.rest import Client


def get_crypto_data(user_arguments):

    print('get crypto dcata user_args: '+user_arguments)
    args = [i.upper() for i in user_arguments[1:]]
    coins = ','.join(args)
    now = datetime.now()
    current_datetime = now.strftime("%m/%d/%Y, %H:%M")
    current_time = now.strftime("%H:%M")
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
        # print('tweet: ' + tweet)
        # return tweet

    except KeyError as err:
        tweet = 'The ticker: ' + str(err) + ' is invalid'
        print(str(err))
        cancel_tweet = False

    except Exception as err:
        print(str(err))

    return tweet


def get_stock_data(user_arguments):

    user_stock = user_arguments[1]

    try:
        r = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + user_stock + '&token=brkpvdvrh5r8d4o95bf0').json()

        stock_message = user_stock + " prices:"
        current_price = "   Current Price: " + str(r["c"])
        day_high = "   High of the day: " + str(r["h"])
        day_low = "   Low of the day: " + str(r["l"])
        current_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M")

        tweet = ('Prices are in USD as of ' + str(current_datetime))

        for price_message in [stock_message, current_price, day_high, day_low]:
            tweet += '\n' + price_message

        print(tweet)

        return tweet

    except Exception as err:
        print(str(err))


def tweet_data(message):

    print(message)

    with open('credentials.json') as f:
        credentials = json.load(f)

        api_key = credentials['Twitter']['apiKey']
        api_secret = credentials['Twitter']['apiSecret']
        access_token = credentials['Twitter']['accessToken']
        access_token_secret = credentials['Twitter']['accessTokenSecret']

        api = Twython(api_key,
                      api_secret,
                      access_token,
                      access_token_secret)

        api.update_status(status=message)

        print("The message has been tweeted. Tweet: ")
        print(message)


def text_data(message):

    # open json file to read information to text
    with open('credentials.json') as f:
        credentials = json.load(f)

        account_SID = credentials['Text']['accountSID']
        authorization_token = credentials['Text']['authToken']
        twilio_number = credentials['Text']['myTwilioNumber']
        cellphone_number = credentials['Text']['myCellPhone']

        twilioCli = Client(account_SID, authorization_token)
        twilioCli.messages.create(
            body=message, from_=twilio_number, to=cellphone_number)

        print("A text has been sent to: %s. Message:" % cellphone_number)
        print(message)


def message_method(option, message):

    print('msg method: msg: ' + str(message))
    if option == 'tw':
        tweet_data(message)

    else:
        text_data(message)


# def google_sheets_update(data):

#     counter = 1

#     for index, value in enumerate(data, 1):

#         worksheet.update_cell(counter, idx, value)
#         counter += 1
#         print(value)


def main():

    market_option = input(
        "Enter 'c' if you would to receive or tweet cryptocurrency messages or 's' for stock market messages...\n")

    if (market_option != 'c' and market_option != 's'):
        market_option = input(
            "That is not a valid option. Please input 'c' for cryptocurrency or 's' for stock market.")

    message_option = input(
        "Enter 'tw' if you would tweet messages or 'tx' to text message...\n")

    if (message_option != 'tw' and message_option != 'tx'):
        message_option = input(
            "That is not a valid option. Please input 'tw' for tweets or 'tx' for text messages.")

    if market_option == 'c':

        try:
            print()
            print(
                "Please enter a time interval to send messages and your desired cryptocurrencies \n")
            print("[minute(s)] [coin symbol] [..coin symbol]..")
            print("Example 1: 1 BTC")
            crypto_args = input("Example 2: 5 ETH BTC LTC: ")
            message = get_crypto_data(crypto_args)
            print(message)
            message_method(message_option, message)

        except Exception as err:
            print(str(err))

    else:

        try:
            print()
            print(
                "Please enter a time interval to send messages and your desired cryptocurrencies \n")
            print("Only 1 stock is supported at this time.\n")
            print("[minute(s)] [stock ticker]")
            print("Example 1: 1 AAPL")
            stock_args = input("Example 2: 5 NVDA")
            message = get_stock_data(stock_args)

            message_method(message_option, message)

        except Exception as err:
            print(str(err))

        # try:
        #     print("hello")
        #     # schedule.every(0.5).minutes.do(tweet_prices)
        #     # schedule.every(float(sys.argv[1])).minutes.do(tweet_prices)

        #     tweet_prices()

        # while True:

        # Checks whether a scheduled task
        # is pending to run or not
        # schedule.run_pending()
        # time.sleep(1)

    # except Exception as err:

    #     print()
    #     print('Usage: python crypto-price-script <min> <coin> <coin>*')
    #     print('<min>: required, must be a number')
    #     print('<coin>: required, valid coin ticker e.g. BTC ETH')
    #     print('<coin>* may use more than 1 coin')
    #     print()
    #     print('e.g. python crypto-price-script 5 BTC ETH')
    #     print('This will tweet the price of BTC and ETH every 5 minutes to:'
    #           ' https://twitter.com/script_crypto')
    #     print('hahsahsa' + str(err))


if __name__ == "__main__":
    main()
