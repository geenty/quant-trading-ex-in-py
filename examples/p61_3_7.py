"""
Example 3.7: A Simple Mean Reverting Model with and without
    transaction costs.
    S&P list available at www.standardandpoors.com
pg 61
"""

import numpy as np
import pandas as pd

# testing this strategy for 2006
start_date = 20060101
end_date = 20061231

spx_df = pd.read_table('data/SPX_20071123.txt')  # data provided from site
spx_df['Date'] = spx_df['Date'].astype('int')
spx_df.set_index('Date', inplace=True)
spx_df.sort_index(inplace=True)

# calculations
daily_return = spx_df.pct_change()  # daily returns
market_daily_return = daily_return.mean(axis=1)  # equal weighted market index returns

weights = -(np.array(daily_return)
            - np.array(market_daily_return).reshape((daily_return.shape[0], 1))
            )  # weight of a stock is proportional to the negative distance to the market index

#  those stocks that do not have valid prices or daily returns are excluded
weight_sum = np.nansum(abs(weights), axis=1)
weights[weight_sum == 0, ] = 0
weight_sum[weight_sum == 0] = 1
weights = weights / weight_sum.reshape((daily_return.shape[0], 1))

daily_pnl = np.nansum(np.array(pd.DataFrame(weights).shift()) * np.array(daily_return), axis=1)
# filter for just our dates of interest
daily_pnl = daily_pnl[np.logical_and(spx_df.index >= start_date, spx_df.index <= end_date)]

sharpe_ratio = np.sqrt(252) * np.mean(daily_pnl) / np.std(daily_pnl)


# now include transaction costs
one_way_t_cost = 0.0005  # 5 bps
weights = weights[np.logical_and(spx_df.index >= start_date, spx_df.index <= end_date)]
daily_pnl_minus_t_cost = daily_pnl - (np.nansum(abs(weights - np.array(pd.DataFrame(weights).shift())), axis=1)
                                      * one_way_t_cost)

sharpe_ratio_minus_t_cost = np.sqrt(252) * np.mean(daily_pnl_minus_t_cost) \
                            / np.std(daily_pnl_minus_t_cost)

