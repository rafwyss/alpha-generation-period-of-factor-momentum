import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Additional Python-Script Nr. 1a
********************************************************************
STATISTICAL ANALYSIS OF THE UNDERLYING FACTOR RETURN DATA
"""

#read relevant CSV file into python
df = pd.read_csv("USA_factor_returns_since_1971-11-30.csv")

# Set the earliest_period parameter equal to the first file.
earliest_period = '1971-11-30'


#STATISTIC MEASURES OF THE UNDERLYING DATA
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

stats_return_weighting = pd.DataFrame(columns=['return weighting scheme', 'count', 'mean', 'median', 'std', 'var', 'min', '25%', '75%', 'max', 'skew',
                 'kurt'], index=[0])
stats_return_weighting.iloc[0, :] = 0

for i in range(0, len(returns_weighting_list)):

    #STATISTICS BY RETURN WEIGHTING
    #(including less than 12 months AGPs with a value of 6)
    stats_return_weighting.loc[i,'return weighting scheme'] = returns_weighting_list[i]

    descr = df[f'ret_{returns_weighting_list[i]}'].describe()
    descr.loc['median'] = df[f'ret_{returns_weighting_list[i]}'].median()
    descr.loc['var'] = df[f'ret_{returns_weighting_list[i]}'].var()
    descr.loc['skew'] = df[f'ret_{returns_weighting_list[i]}'].skew()
    descr.loc['kurt'] = df[f'ret_{returns_weighting_list[i]}'].kurt()

    help_list = stats_return_weighting.columns.values.tolist()

    for j in help_list[1:]:
        stats_return_weighting.loc[i, j] = descr.loc[j]

stats_return_weighting.to_csv(f'USA_factor_returns_since_{earliest_period}_statistics.csv', index=False)
