"""
Example 3.1: using Python to  scrape web pages for financial data.
Added additional functionality for changes to yahoo finance.
pg 34
"""

from io import StringIO
import os
import re
import time
import pandas as pd
import requests


# configure here
SYMBOL = 'IBM'
SAVE_DATA = True


def get_yahoo_ticker_data(ticker):
    res = requests.get('https://finance.yahoo.com/quote/' + ticker + '/history')
    yahoo_cookie = res.cookies['B']
    yahoo_crumb = None

    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
    for line in res.text.splitlines():
        m = pattern.match(line)
        if m is not None:
            yahoo_crumb = m.groupdict()['crumb']

    cookie_tuple = yahoo_cookie, yahoo_crumb
    current_date = int(time.time())
    url_kwargs = {'symbol': ticker, 'timestamp_end': current_date,
                  'crumb': cookie_tuple[1]}

    url_price = 'https://query1.finance.yahoo.com/v7/finance/download/' \
                '{symbol}?period1=-3008988800&period2={timestamp_end}&interval=1d&events=history' \
                '&crumb={crumb}'.format(**url_kwargs)

    response = requests.get(url_price, cookies={'B': cookie_tuple[0]})
    return response


if __name__ == "__main__":
    try:
        print(f"Getting data for {SYMBOL}")
        ticker_data = get_yahoo_ticker_data(SYMBOL)
        print(f"Got data for {SYMBOL}. Transforming to DataFrame")
        ticker_df = pd.read_csv(StringIO(ticker_data.text), sep=",")
        print(ticker_df.head())
        print(f"Done with {SYMBOL}. Got data from {ticker_df.Date.min()} to {ticker_df.Date.max()}")

        if SAVE_DATA:
            print("Saving data...")
            save_path = f"data/yahoo/{SYMBOL}/"
            file_name = save_path + f"{ticker_df.Date.min()}_{ticker_df.Date.max()}.csv"

            # create save path if it doesnt exist
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            ticker_df.to_csv(file_name, index=None)
            print(f"Done saving {file_name}.")

    except Exception as e:
        print(f"Failed getting data for {SYMBOL}")
        print(e)
