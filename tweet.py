# import requests
# import alpha_vantage
# import pandas as pd

# df = pd.DataFrame()
# API_URL = "https://www.alphavantage.co/query"

# #symbols= ["IBM", "MSFT", "LVLT"]
# symbols = "IBM,MSFT,LVLT"
# data = {
#     "function": "BATCH_STOCK_QUOTES",
#     "symbols": symbols,
#     "apikey": "XXX",
# }

# response = requests.get(API_URL, params=data)


# print(response.json())

# s = 'mike'

# print('sadsa %s' % s)
import sys
import schedule
# something = input("DSADSADA: ")

# new = something.split(" ")

# print(new[1])

# he = [1, 2, 3, 4, 5, 6]

# print(he[2:])

# market_option = input(
#     "Enter 'c' if you would to receive or tweet cryptocurrency messages or 's' for stock market messages...\n")

# if (market_option != 'c' and market_option != 's'):
#     print('true')
# market_option = input(
#     "That is not a valid option. Please input 'c' for cryptocurrency or 's' for stock market.")

# user_arguments = ['dsadsa', 'cdsaacs', 'cdsacsddsa', 'dsd']
# args = [i.upper() for i in user_arguments[1:]]
# print(args)


def ok():
    return 'hi'


# x = schedule.every(1).minutes.do(ok)
# print(x)

r = ok()
print(r)
