"""
Example 3.4: Calculating Sharpe Ratio for Long-only
            Versus Market-Neutral Strategies
pg 45
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read in data from provided file IGE.xls
df = pd.read_excel('data/IGE.xls')
df.sort_values(by='Date', inplace=True)

# long-only calculations
daily_returns = df.loc[:, 'Adj Close'].pct_change()
excess_returns = daily_returns - 0.04 / 252  # assuming risk-free rate of 4% annually
sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)


# bring in the broader market data
# read in data from provided file SPY.xls
df_two = pd.read_excel('data/SPY.xls')
df = pd.merge(df, df_two, on='Date', suffixes=('_IGE', '_SPY'))
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# market-neutral calculations
daily_returns = df[['Adj Close_IGE', 'Adj Close_SPY']].pct_change()
daily_returns.rename(columns={"Adj Close_IGE": "IGE", "Adj Close_SPY": "SPY"}, inplace=True)
net_returns = (daily_returns['IGE'] - daily_returns['SPY']) / 2
sharpe_ratio = np.sqrt(252) * np.mean(net_returns) / np.std(net_returns)
cumulative_returns = np.cumprod(1 + net_returns) - 1
plt.plot(cumulative_returns)
plt.show()  # for pyCharm


# adding 3.5 below

# create a function to find the max drawdown given a series of returns

def get_max_drawdown(cumulative_return_series):
    """
    calculation of maximum drawdown and maximum drawdown duration based on
    cumulative compound returns
    :param cumulative_return_series: array of compounded cumulative return
    :return: max drawdown, max drawdown duration
    """
    high_water_mark = np.zeros(cumulative_return_series.shape)
    drawdown = np.zeros(cumulative_return_series.shape)
    drawdown_duration = np.zeros(cumulative_return_series.shape)

    for t in np.arange(1, cumulative_return_series.shape[0]):
        high_water_mark[t] = np.maximum(high_water_mark[t - 1], cumulative_return_series[t])
        drawdown[t] = (1 + cumulative_return_series[t]) / (1 + high_water_mark[t]) - 1
        if drawdown[t] == 0:
            drawdown_duration[t] = 0
        else:
            drawdown_duration[t] = drawdown_duration[t - 1] + 1

    max_dd, i = np.min(drawdown), np.argmin(drawdown)  # drawdown < 0 always
    max_ddd = np.max(drawdown_duration)

    return max_dd, max_ddd, i


# get the stats on the spy adjusted data
max_drawdown, max_drawdown_duration, start_drawdown_day = get_max_drawdown(cumulative_returns.values)
