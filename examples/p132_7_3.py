"""
Example 7.3: Testing the Cointegration versus Correlation
    properties between KO and PEP
pg 132
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
from statsmodels.api import OLS
from scipy.stats import pearsonr


df_ko = pd.read_excel('data/KO.xls')  # provided
df_pep = pd.read_excel('data/PEP.xls')

df = pd.merge(df_ko, df_pep, on='Date', suffixes=('_KO', '_PEP'))
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)


# Run cointegration (Engle-Granger) test as cadf was returning problems
coint_t, p_value, crit_value = coint(df['Adj Close_KO'], df['Adj Close_PEP'])
(coint_t, p_value, crit_value) # abs(t-stat) < critical value at 90%.
#  pvalue says probability of null hypothesis (of no cointegration) is 73%


#  Determine hedging ratio
model = OLS(df['Adj Close_KO'], df['Adj Close_PEP'])
results = model.fit()
hedge_ratio = results.params


#  spread = KO - hedgeRatio*PEP
spread = df['Adj Close_KO'] - hedge_ratio[0] * df['Adj Close_PEP']

plt.plot(spread)
plt.show()  # for Pycharm


# Correlation test
daily_returns = df.loc[:, ('Adj Close_KO', 'Adj Close_PEP')].pct_change()
daily_returns.corr()
daily_returns_clean = daily_returns.dropna()

pearsonr(daily_returns_clean.iloc[:, 0], daily_returns_clean.iloc[:, 1])

# first output is correlation coefficient, second output is pvalue.