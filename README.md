# Crypto-Twitter-Bot

A Python bot that tweets out the prices of selected cryptocurrencies or a stock price and inputs data into a spreadsheet every desired number of minutes (work in progress). Currently only one stock is supported on a free account. For the credentials aspect, ensure that you have a Twitter, Twilio and Finnhub account!

Example usage: 

`python market-price-bot.py`

You will then be given the message to select if you would like to input cryptocurrencies or a stock.

`Enter 'c' if you would to receive or tweet cryptocurrency messages or 's' for stock market messages...`

After inputting 'c' or 's' you will be given a message to select if you would like receive texts or to tweet.

`Enter 'tw' if you would tweet messages or 'tx' to text message...`

Afterwards, if you chose 'c' for cryptocurrency you will be asked to input a time interval and cryptocurrencies in the following format.

`[minute(s)] [coin symbol] *[coinsymbol]`

If you chose 's', you will be asked to input a similar format shown below:

`[minute(s)] [stock ticker]`

Examples of the tweets are shown [here](https://twitter.com/script_crypto)

An example of the text is shown [here](https://pbs.twimg.com/media/EaxH3jtUEAEs5Do?format=jpg&name=small)
