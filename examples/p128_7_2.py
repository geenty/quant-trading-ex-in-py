"""
Example 7.2: How to Form a Good Cointegrating
    (and Mean-reverting) Pair of Stocks
    using the cointegrating augmented Dickey-Fuller (cadf) and coint
pg 128
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
from statsmodels.api import OLS


df_gld = pd.read_excel('data/GLD.xls')  # provided
df_gdx = pd.read_excel('data/GDX.xls')

df = pd.merge(df_gld, df_gdx, on='Date', suffixes=('_GLD', '_GDX'))
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)


#  Run cointegrating augmented Dickey-Fuller
# X = df[['Adj Close_GLD','Adj Close_GDX']].values
# result = adfuller(X)
# coint_t, p_value, crit_value = adfuller(X)
#
# adfstat, pvalue, critvalues, resstore = ts.adfuller(y.y,regression='c',store=True,regresults=True)
# Having issues with adfuller and using Engle-Granger instead

#  Run cointegration (Engle-Granger) test

coint_t, p_value, crit_value = coint(df['Adj Close_GLD'], df['Adj Close_GDX'])

(coint_t, p_value, crit_value) # abs(t-stat) > critical value at 95%.
# p_value says probability of null hypothesis (of no cointegration) is only 1.8%]

#  Determine hedging ratio
model = OLS(df['Adj Close_GLD'], df['Adj Close_GDX'])
results = model.fit()
hedge_ratio = results.params

#  spread = GLD - hedge_ratio * GDX
spread = df['Adj Close_GLD'] - hedge_ratio[0] * df['Adj Close_GDX']

plt.plot(spread)
plt.show()  #  For pyCharm
