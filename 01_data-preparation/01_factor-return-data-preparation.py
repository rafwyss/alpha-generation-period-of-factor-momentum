import pandas as pd
import os

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
data set found on Dropbox: 
https://www.dropbox.com/sh/xq278bryrj0qf9s/AACovLXgnTXWHiPvLZ5_umu7a/Country%20Factors?dl=0&subfolder_nav_tracking=1
"""

# Specify the earliest period you want to analyse.
# The earliest possible period is '1971-11-30'
earliest_period = '1971-11-30'

#Reading CSV file into python
fulldf = pd.read_csv("../USA.csv")

# Only the relevant columns 'characteristic', 'eom' and the returns are needed
full_df = fulldf[['characteristic', 'eom', 'ret_ew', 'ret_vw', 'ret_vw_cap']]

# Returns data is only needed going back to the earliest relevant date.
df = full_df.loc[full_df['eom'] >= earliest_period]

# Resetting the index
df.reset_index(drop=True, inplace=True)

# Saving the new data set with all relevant data to a new CSV-file (for security).
df.to_csv(f'USA_factor_returns_since_{earliest_period}.csv', index=False)
print(f'CSV-file saved under name: USA_factor_returns_since_{earliest_period}.csv')

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Specify the return weighting methods you want!
# IF YOU ONLY WANT ONE TYPE OF RETURN WEIGHTING, COMMENT OUT THE OTHERS!!!
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Exporting the resulting data frame!
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