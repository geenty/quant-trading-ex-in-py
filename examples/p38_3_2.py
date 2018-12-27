"""
Example 3.2: Adjusting for Splits and Dividends.
pg 38
"""

import pandas as pd

# as a precursor we will get data for IGE from yahoo finance
IGE_FILE = 'data/yahoo/IGE/2001-11-26_2018-12-24.csv'
raw_df = pd.read_csv(IGE_FILE)

# look at the data surrounding the example date, June 9, 2005
raw_df[(raw_df.Date > '2005-06-01') & (raw_df.Date < '2005-06-25')]

# there was a stock split on 2006-06-09
split_date = '2005-06-09'
share_number = 2.0
raw_df['manually_adjusted_close'] = raw_df.apply(
    lambda row: (row.Close/share_number) if row.Date < split_date else row.Close, axis=1)

# skipping the dividend distribution portion as the data will differ from the example
# due to additional distributions
