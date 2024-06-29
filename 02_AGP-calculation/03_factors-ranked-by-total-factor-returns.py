import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 3
********************************************************************
SORTING OUT THE FACTORS WITH THE HIGHEST RETURNS FOR ALL SPECIFIC
WEIGHTING SCHEMES AND LBP-LENGTHS OVER ALL RELEVANT TIMEFRAMES
********************************************************************
In this file the factors are sorted for the highest returns over the 
look-back period. The dataset produced in this file is then used to
create the factor momentum portfolios.
"""

""" IMPORTANT: CODE ONLY WORKS IF THERE IS A 'total_lbp_ret{}.csv' FILE WITH SPECIFIED WEIGHTING METHOD IN THE DIRECTORY"""

# To save running time and memory, specify the maximum amount of factors you will want to invest in.
# Options: 77 ≈ 50%; 51 = 33.33%; 30 ≈ 20%;
max_amt_factors = 51

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Configure the weighting methods to your liking.

# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lengths over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]


""" START OF THE ANALYSIS"""

# Iterating through all return weighting methods
for x in returns_weighting_list:
    # Iterating through all LBP lengths
    for y in lbp_length_mths_list:
        # Importing the dataset
        df = pd.read_csv(os.path.join('02_total-LBP-factor-returns',f'total_lbp_ret_{x}_{y}mths.csv'))

        # Creating a list with all eom dates
        eom_dates = df.columns.values.tolist()
        eom_dates.pop(0)

        # Creating a new dataframe to store the results
        res_df = df.copy()
        # The headers must only be the eom dates. Therefore, the additional column with the factor names is dropped.
        res_df = res_df.drop(columns='characteristic')
        # Rows are only needed in the quantity of the maximum amount of factors.
        res_df = res_df.iloc[0:max_amt_factors, :]
        # To save memory all values are set to 0
        res_df.iloc[:, :] = 0

        # Changing the type of the data in the results data frame to strings, to store the string-type factor names
        res_df[eom_dates[0:len(eom_dates)]] = res_df[eom_dates[0:len(eom_dates)]].astype(str)

        # Iterating through all columns representing all end-of-LBP dates
        for i in range(0, len(eom_dates)):
            # Sorting the data frame by the highest-returns in the column of the specific end-of-LBP date
            df = df.sort_values(eom_dates[i], ascending=False)
            # Resetting the indices to properly access all rows by the indices
            df.reset_index(drop=True, inplace=True)
            # Iterating through all 153 rows of factors
            for j in range(0, max_amt_factors):
                # Storing the factor-name of each row in the results data frame
                res_df.iloc[j, i] = df['characteristic'][j]


        # Exporting the resulting data frame!
        if export_type == 'csv':
            res_df.to_csv(os.path.join('03_factors-ranked-by-total-factor-returns', f'factors_ranked_by_total_factor_returns_{x}_{y}mths.csv'))
            print(f'CSV-file saved under name: factors_ranked_by_total_factor_returns_{x}_{y}mths.csv')
        elif export_type == 'excel':
            res_df.to_excel(os.path.join('03_factors-ranked-by-total-factor-returns', f'factors_ranked_by_total_factor_returns_{x}_{y}mths.xlsx'))
            print(f'Excel-file saved under name: factors_ranked_by_total_factor_returns_{x}_{y}mths.xlsx')
        elif export_type == 'both':
            res_df.to_csv(os.path.join('03_factors-ranked-by-total-factor-returns', f'factors_ranked_by_total_factor_returns_{x}_{y}mths.csv'))
            res_df.to_excel(os.path.join('03_factors-ranked-by-total-factor-returns', f'factors_ranked_by_total_factor_returns_{x}_{y}mths.xlsx'))
            print(f'CSV- and Excel-files saved under names: factors_ranked_by_total_factor_returns_{x}_{y}mths.format')
        else:
            print('Export file type wrong!!')
