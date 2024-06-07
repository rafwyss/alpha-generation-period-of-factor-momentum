import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
----------------------------------------------------------------------
Python-Script Nr. 5
**********************************************************************
CALCULATING THE TRAILING-TWELVE MONTHS RETURNS OF THE FACTOR PORTFOLIO
**********************************************************************
We adjust the previously calculated factor portfolio returns to be the
factor portfolio returns over the trailing-twelve months on the date 
of the last month.
"""

# Specify how many factors you want to have in the different portfolios
amt_factors_list = [51,
                    30, 15, 7
                    ]

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Please configure the weighting schemes to your liking.
# IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR SPECIFIED WEIGHTING SCHEME IN THE DIRECTORY
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

#IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR LBP-LENGTH IN THE DIRECTORY
# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [#12, 24, 36, 48,
                        60,
                        #72, 84, 96, 108, 120
                        ]

# START OF THE ANALYSIS

for x in returns_weighting_list:
    for y in lbp_length_mths_list:
        for z in amt_factors_list:
            # Importing the relevant file with the corresponding factor portfolio returns for each simulation period.
            ret_df = pd.read_csv(f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv')
            ret_df.set_index('sim_start_dates', inplace=True)
            eom_dates = ret_df.columns.values.tolist()

            # Preparing a new data frame to store the results. It will need to have all the columns but only need rows
            # from the earliest simulation period where we will have 12 months of simulation returns, We therefore can
            # delete 11 rows
            res_df = ret_df.copy()
            res_df = res_df.iloc[11:]
            sim_dates = res_df.index.tolist()

            # Setting all values in the results data frame to 0
            res_df.iloc[0:,0:] = 0



            # START OF THE ANALYSIS
            ttm_ret = 1
            # Iterating over all end of LBP dates
            for i in range(0, len(eom_dates)):
                # Iterating over all simulation period dates
                for j in range(i, len(sim_dates)):
                    # Iterating over 12 returns to compound them to a 12 months return
                    for k in range(0, 12):
                        # Calculating the TRAILING TWELVE MONTHS RETURN AS A COMPOUNDED RETURN (PRODUCT of 1 + return)
                        ttm_ret = ttm_ret * (1 + ret_df.iloc[j + k, i])
                    res_df.iloc[j,i] = ttm_ret - 1
                    ttm_ret = 1

            # EXPORTING THE RESULTING DATA FRAME!
            if export_type == 'csv':
                res_df.to_csv(f'sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.csv')
                print(f'CSV-file saved under name: sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.csv')
            elif export_type == 'excel':
                res_df.to_excel(f'sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
                print(f'Excel-file saved under name: sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
            elif export_type == 'both':
                res_df.to_csv(f'sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.csv')
                res_df.to_excel(f'sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
                print(
                    f'CSV- and Excel-files saved under names: sim_ttm_pf_returns_{x}_{y}mths_{z}fctr.format')
            else:
                print('Export file type wrong!!')
