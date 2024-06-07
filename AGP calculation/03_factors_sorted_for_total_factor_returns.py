import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 3
********************************************************************
SORTING OUT THE FACTORS WITH THE HIGHEST RETURNS FOR ALL SPECIFIC
WEIGHTING SCHEMES AND LBP-LENGTHS OVER ALL RELEVANT TIMEFRAMES
********************************************************************
In this file we sort the factors with the highest returns over the 
look-back period. The dataset produced in this file will be used to
create the factor portfolios.
"""

# To save time and memory, specify the maximum amount of factors you will want to invest in.
# Options: 77 ≈ 50%; 51 = 33.33%; 30 ≈ 20%;
max_amt_factors = 51

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Please configure the weighting schemes to your liking.
""" IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR SPECIFIED WEIGHTING SCHEME IN THE DIRECTORY"""
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

""" IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR LBP-LENGTH IN THE DIRECTORY"""
# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48,
                        60,
                        72, 84, 96, 108, 120
                        ]


""" START OF THE ANALYSIS"""

for x in returns_weighting_list:
    for y in lbp_length_mths_list:
        # Import the dataset
        df = pd.read_csv(f'total_lbp_ret_{x}_{y}mths.csv')
        #print(df)

        # Create a list with all eom dates
        eom_dates = df.columns.values.tolist()
        eom_dates.pop(0)

        # Create a new dataframe to store the results
        res_df = df.copy()
        # The headers must only be the eom dates. Therefore we drop the additional column with the factor names
        res_df = res_df.drop(columns='characteristic')
        # We only need rows in the quantity of the maximum amount of factors
        res_df = res_df.iloc[0:max_amt_factors, :]
        # To save memory we can set all values to 0
        res_df.iloc[:, :] = 0

        # Changing the type of the data in the results data frame to strings, to store the string-factor names without an error
        res_df[eom_dates[0:len(eom_dates)]] = res_df[eom_dates[0:len(eom_dates)]].astype(str)



        # Iterating through all columns representing all end-of-LBP dates
        for i in range(0, len(eom_dates)):
            # Sorting the data frame by the highest-returns in the column of the specific end-of-LBP date
            df = df.sort_values(eom_dates[i], ascending=False)
            # resetting the indices to properly access all rows to store the values
            df.reset_index(drop=True, inplace=True)
            # Iterating through all 153 rows of factors and storing the factor-name of each row in the results data frame
            for j in range(0, max_amt_factors):
                res_df.iloc[j, i] = df['characteristic'][j]




        #EXPORTING THE RESULTING DATA FRAME!
        if export_type == 'csv':
            res_df.to_csv(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.csv')
            print(f'CSV-file saved under name: factors_sorted_for_total_factor_returns_{x}_{y}mths.csv')
        elif export_type == 'excel':
            res_df.to_excel(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.xlsx')
            print(f'Excel-file saved under name: factors_sorted_for_total_factor_returns_{x}_{y}mths.xlsx')
        elif export_type == 'both':
            res_df.to_csv(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.csv')
            res_df.to_excel(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.xlsx')
            print(f'CSV- and Excel-files saved under names: factors_sorted_for_total_factor_returns_{x}_{y}mths.format')
        else:
            print('Export file type wrong!!')
