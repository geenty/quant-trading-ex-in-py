"""
Example 3.6: Pairs Trading of GLD and GDX
pg 55
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


# import data provided
df_gld = pd.read_excel('data/GLD.xls')
df_gdx = pd.read_excel('data/GDX.xls')

df = pd.merge(df_gld, df_gdx, on='Date', suffixes=('_GLD', '_GDX'))
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

# create training and testing skeleton
trainset = np.arange(0, 252)
testset = np.arange(trainset.shape[0], df.shape[0])

# back into a good hedging ratio
model = sm.OLS(df.loc[:, 'Adj Close_GLD'].iloc[trainset],
               df.loc[:, 'Adj Close_GDX'].iloc[trainset]
               )
results = model.fit()
hedge_ratio = results.params

# use that hedging ratio to figure out the spread over time
spread = df.loc[:, 'Adj Close_GLD'] - hedge_ratio[0] * df.loc[:, 'Adj Close_GDX']

plt.plot(spread.iloc[trainset])
plt.show()  # for pyCharm

plt.plot(spread.iloc[testset])
plt.show()  # for pyCharm

spread_mean = np.mean(spread.iloc[trainset])
spread_std = np.std(spread.iloc[trainset])
df['zscore'] = (spread - spread_mean) / spread_std

# create empty cols for backtest
df['positions_GLD'] = np.nan
df['positions_GDX'] = np.nan

df.loc[df.zscore >= 2, ('positions_GLD', 'positions_GDX')] = [-1, 1] # Buy spread
df.loc[df.zscore <= -2, ('positions_GLD', 'positions_GDX')] = [1, -1] # Short spread
df.loc[abs(df.zscore) <= 1, ('positions_GLD', 'positions_GDX')] = 0 # Exit spread
df.fillna(method='ffill', inplace=True) # ensure existing positions are carried forward unless there is an exit signal

positions = df.loc[:, ('positions_GLD', 'positions_GDX')]
daily_returns = df.loc[:, ('Adj Close_GLD', 'Adj Close_GDX')].pct_change()
pnl = (np.array(positions.shift()) * np.array(daily_returns)).sum(axis=1)

sharpe_trainset = np.sqrt(252) * np.mean(pnl[trainset[1:]]) / np.std(pnl[trainset[1:]])
sharpe_testset = np.sqrt(252) * np.mean(pnl[testset]) / np.std(pnl[testset])

plt.plot(np.cumsum(pnl[testset]))
plt.show()  # for pyCharm

