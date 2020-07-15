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


# Get the crypto message
def get_crypto_data(user_arguments):

    user_coins = user_arguments.split(" ")
    args = [i.upper() for i in user_coins[1:]]
    coins = ','.join(args)
    now = datetime.now()
    current_datetime = now.strftime("%m/%d/%Y, %H:%M")
    current_time = now.strftime("%H:%M")
    data = {}
    currency = 'USD'

    try:
        r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=' +
                         coins + '&tsyms=' + currency).json()
        message = ('Prices are in ' + currency +
                   ' as of ' + str(current_datetime))
        data["current_time"] = current_time

        for index, arg in enumerate(args, 0):
            line = str(arg + ': ' + str(r[arg][currency]))
            message = message + '\n' + "  " + line
            data[arg] = r[arg][currency]

        # populate_cells(data)
        # return message

    except KeyError as err:
        message = 'The ticker: ' + str(err) + ' is invalid'
        print(str(err))
        cancel_message = False

    except Exception as err:
        print(str(err))

    return message


# Get the stock message
def get_stock_data(user_arguments):

    with open('credentials.json') as f:
        credentials = json.load(f)

    stock_token = credentials["Finnhub"]["token"]
    user_stock = user_arguments.split(" ")[1].upper()

    try:
        r = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + user_stock + '&token=' + stock_token).json()

        day_prices = "  C: %s | H: %s | L: %s" % (
            str(r["c"]), str(r["h"]), str(r["l"]))

        percent_change = round((r["c"] / r["pc"]), 4)
        dollar_calc = r["c"] - r["pc"]

        if percent_change > 1:
            percent_calc = round(((percent_change - 1) * 100), 3)
            # dollar_change = "+%s" % dollar_calc
            # percentage = str(percent_calc) + " ↑"
            # total_change_message =
            total_change_message = "+{:.2f} ({}%) ↑".format(dollar_calc,
                                                            percent_calc)
        else:
            percent_calc = round(((1 - percent_change) * 100), 3)
            # dollar_change = "-%s" % dollar_calc
            # percentage = "(%s) ↓" % str(percent_calc)
            total_change_message = "{:.2f} ({}%) ↓".format(dollar_calc,
                                                           percent_calc)

        percent_message = "  Chg: {} | Prev. Close: {}".format(
            total_change_message, r['pc'])

        current_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M")
        message = ('$%s data as of %s' %
                   (user_stock, str(current_datetime)))

        for price_message in [day_prices, percent_message]:
            message += '\n' + price_message

        return message

    except Exception as err:
        print(str(err))


# Tweet the stock or cryptocurreny message
def tweet_data(message):

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

        # print("The message has been tweeted. Tweet: ")


# Text the stock or cryptocurrency message
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

        # print("A text has been sent to: %s. Message:" % cellphone_number)


def message_method(message_option, market_option, user_args):

    if message_option == 'tw':
        if market_option == 'c':
            tweet_data(get_crypto_data(user_args))

        else:
            tweet_data(get_stock_data(user_args))

    else:
        if market_option == 'c':
            text_data(get_crypto_data(user_args))

        else:
            text_data(get_stock_data(user_args))


# def google_sheets_update(data):

#     counter = 1

#     for index, value in enumerate(data, 1):

#         worksheet.update_cell(counter, idx, value)
#         counter += 1
#         print(value)


def main():

    market_option = input(
        "Enter 'c' if you would to receive or tweet cryptocurrency messages or 's' for stock market messages...\nInput: ")

    if (market_option != 'c' and market_option != 's'):
        market_option = input(
            "That is not a valid option. Please input 'c' for cryptocurrency or 's' for stock market. \nInput: ")

    message_option = input(
        "Enter 'tw' if you would tweet messages or 'tx' to text message...\nInput: ")

    if (message_option != 'tw' and message_option != 'tx'):
        message_option = input(
            "That is not a valid option. Please input 'tw' for tweets or 'tx' for text messages. \nInput: ")

    if market_option == 'c':

        try:
            print()
            print(
                "Please enter a time interval to send messages and your desired cryptocurrencies \n")
            print("[minute(s)] [coin symbol] [..coin symbol]..")
            print("Example 1: 1 BTC")
            print("Example 2: 5 ETH BTC LTC")
            user_arguments = input("Input: ")

        except Exception as err:
            print(str(err))

    else:

        try:
            print()
            print(
                "Please enter a time interval to send messages and your desired stock")
            print("Only 1 stock is supported at this time.\n")
            print("[minute(s)] [stock ticker]")
            print("Example 1: 1 AAPL")
            print("Example 2: 4 NVDA")
            user_arguments = input("Input: ")

        except Exception as err:
            print(str(err))

    try:

        schedule.every(int(user_arguments.split(" ")[0])).minutes.do(
            message_method, message_option, market_option, user_arguments)

        # For testing
        # message_method("tw", "s", user_arguments)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as err:
        print(str(err))


if __name__ == "__main__":
    main()
