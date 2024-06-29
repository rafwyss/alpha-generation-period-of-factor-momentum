import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Additional Python Script NR. 3a
********************************************************************
CREATING THE SPECIFIC FACTOR MOMENTUM PORTFOLIOS FOR DIFFERENT 
PERCENTILES
********************************************************************
"""

""" IMPORTANT: CODE ONLY WORKS IF THERE IS A 'total_lbp_ret{}.csv' FILE WITH SPECIFIED WEIGHTING METHOD IN THE DIRECTORY"""

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

amt_factors_list = [51, 30, 15, 7,
                    ]

# Configure the weighting schemes to your liking.
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew',
                          'vw', 'vw_cap'
                          ]

# Specify all Look-back-period lengths!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

""" START OF THE ANALYSIS"""

# Iterating through all return weighting methods
for x in returns_weighting_list:
    # Iterating through all LBP lengths
    for y in lbp_length_mths_list:
        # Iterating over all percentiles of factors.
        for z in amt_factors_list:
            # Importing the dataset
            df = pd.read_csv(os.path.join('03_factors-ranked-by-total-factor-returns',f'factors_ranked_by_total_factor_returns_{x}_{y}mths.csv', index_col=0))

            # Creating the results data frame
            res_df = df.copy()

            # Only taking the amount of factors specified above.
            res_df = res_df.iloc[:z,:]


            # Exporting the resulting data frame!
            if export_type == 'csv':
                res_df.to_csv(os.path.join('03a_factor-momentum-portfolios',f'factor_portfolio_{x}_{y}mths_{z}fctrs.csv'))
                print(f'CSV-file saved under name: factor_portfolio_{x}_{y}mths_{z}fctrs.csv')
            elif export_type == 'excel':
                res_df.to_excel(os.path.join('03a_factor-momentum-portfolios',f'factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx'))
                print(f'Excel-file saved under name: factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx')
            elif export_type == 'both':
                res_df.to_csv(os.path.join('03a_factor-momentum-portfolios',f'factor_portfolio_{x}_{y}mths_{z}fctrs.csv'))
                res_df.to_excel(os.path.join('03a_factor-momentum-portfolios',f'factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx'))
                print(f'CSV- and Excel-files saved under names: factor_portfolio_{x}_{y}mths_{z}fctrs.format')
            else:
                print('Export file type wrong!!')
