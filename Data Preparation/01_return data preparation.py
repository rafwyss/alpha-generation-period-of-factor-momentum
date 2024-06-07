import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 1
********************************************************************
TRANSFORMING THE FACTOR RETURNS DATA INTO A PIVOT TABLE FORMAT TO BE
USED IN ALL FURTHER CALCULATIONS
********************************************************************
All further analysis will be conducted on the data generated from 
this file.
--------------------------------------------------------------------
The main data set used in this paper is the JKP "USA" factor returns
data set found in the Dropbox: https://www.dropbox.com/sh/xq278bryrj0qf9s/AACovLXgnTXWHiPvLZ5_umu7a/Country%20Factors?dl=0&subfolder_nav_tracking=1
"""

# Specify the earliest period you want to analyse.
# The earliest possible period is '1971-11-30'
earliest_period = '1971-11-30'

#read CSV file into python
fulldf = pd.read_csv("USA.csv")

# We only need the relevant columns 'characteristic', 'eom' and the returns
full_df = fulldf[['characteristic', 'eom', 'ret_ew', 'ret_vw', 'ret_vw_cap']]

# We also need returns data going back to the earliest relevant date.
df = full_df.loc[full_df['eom'] >= earliest_period]

# Reset the index
df.reset_index(drop=True, inplace=True)

# Saving the new data set with all relevant data to a new CSV-file (for security).
df.to_csv('USA_factor_returns_since_11_1971.csv', index=False)

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Specify the return weighting schemes you want!
#IF YOU ONLY WANT ONE TYPE OF RETURN WEIGHTING, COMMENT OUT THE OTHERS!!!
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

for x in range(0,len(returns_weighting_list)):
    ret_df = pd.pivot_table(df, values=f'ret_{returns_weighting_list[x]}', index='characteristic', columns='eom')
    if export_type == 'csv':
        ret_df.to_csv(f'ret_{returns_weighting_list[x]}_pivot.csv')
        print(f'CSV-file saved under name: ret_{returns_weighting_list[x]}_pivot.csv')
    elif export_type == 'excel':
        ret_df.to_excel(f'ret_{returns_weighting_list[x]}_pivot.xlsx')
        print(f'Excel-file saved under name: ret_{returns_weighting_list[x]}_pivot.xlsx')
    elif export_type == 'both':
        ret_df.to_excel(f'ret_{returns_weighting_list[x]}_pivot.xlsx')
        print(f'CSV- and Excel-file saved under name: ret_{returns_weighting_list[x]}_pivot.format')
    else:
        print('Export file type wrong!!')



#STATISTIC MEASURES OF THE UNDERLYING DATA
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

# Creating the data frame for the statistics
"""
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

stats_return_weighting.to_csv('USA_factor_returns_since_11_1971_statistics.csv', index=False)
"""