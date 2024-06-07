import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
PYTHON-SCRIPT-NR. 3.2
********************************************************************
SAVING THE FACTOR PORTFOLIOS
********************************************************************

"""

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

amt_factors_list = [
    51, 30, 15, 7,
               5
               ]

# Please configure the weighting schemes to your liking.
""" IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR SPECIFIED WEIGHTING SCHEME IN THE DIRECTORY"""
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew',
                          'vw', 'vw_cap'
                          ]

""" IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR LBP-LENGTH IN THE DIRECTORY"""
# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]


""" START OF THE ANALYSIS"""

for x in returns_weighting_list:
    for y in lbp_length_mths_list:
        for z in amt_factors_list:
            # Import the dataset
            df = pd.read_csv(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.csv')
            df = df.drop(columns=['Unnamed: 0'])

            res_df = df.copy()

            # We only take the amount of factors needed.
            res_df = res_df.iloc[:z,:]


            #EXPORTING THE RESULTING DATA FRAME!
            if export_type == 'csv':
                res_df.to_csv(f'factor_portfolio_{x}_{y}mths_{z}fctrs.csv')
                print(f'CSV-file saved under name: factor_portfolio_{x}_{y}mths_{z}fctrs.csv')
            elif export_type == 'excel':
                res_df.to_excel(f'factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx')
                print(f'Excel-file saved under name: factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx')
            elif export_type == 'both':
                res_df.to_csv(f'factor_portfolio_{x}_{y}mths_{z}fctrs.csv')
                res_df.to_excel(f'factor_portfolio_{x}_{y}mths_{z}fctrs.xlsx')
                print(f'CSV- and Excel-files saved under names: factor_portfolio_{x}_{y}mths_{z}fctrs.format')
            else:
                print('Export file type wrong!!')
