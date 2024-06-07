import pandas as pd

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 4
********************************************************************
CALCULATING THE MONTHLY FACTOR RETURNS OF THE SPECIFIED PORTFOLIO
OF FACTORS WITH THE HIGHEST PERFORMANCE OVER THE LOOK-BACK-PERIOD
********************************************************************
To generate the portfolios, we specify the percentile of factors 
we want to invest in with our strategy.
--------------------------------------------------------------------
153 Factors in Total. Good ptions to include in amt_factors_list:
Top Tercile = 51
Top Quintile: = 30
Top Decile:  = 15
Top 5%: 7
--------------------------------------------------------------------
The factor portfolio returns are calculated with an equally weighted 
return scheme, meaning with rebalancing at the beginning of every 
month.
"""

# Set equal to the amount of factors your factors_sorted_for_total_factor_returns....csv files contain
max_amt_factors = 51

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

for x in returns_weighting_list:
    for y in lbp_length_mths_list:
        for z in amt_factors_list:
            # Importing the relevant file with the sorted factor names (fn)
            fn_df = pd.read_csv(f'factors_sorted_for_total_factor_returns_{x}_{y}mths.csv', index_col=0)

            # Importing the factor returns pivot table file for the specified weighting scheme
            ret_df = pd.read_csv(f'ret_{x}_pivot.csv')
            ret_df.set_index('characteristic', inplace=True)

            # Storing the dates in a list
            eom_dates = fn_df.columns.values.tolist()

            # Making a new list of the simulation period dates to work as the indexes.
            # The simulation dates are not equal to the end of LBP dates, because we are only looking at LBP's until 2021-12-31
            # We can have the simulation period dates up until 2023-12-31, however. Therefore we need to get the sim_dates from a different source: the old pivot table
            sim_dates = ret_df.columns.values.tolist()
            # Deleting the simulation periods which lie prior to the earliest end of a LBP
            sim_dates = sim_dates[y:]


            #Preparing a data frame to store the results
            res_df = fn_df.copy()
            # Setting all values to 0
            res_df.iloc[0:, 0:] = 0
            # Changing the data type to floats
            res_df = res_df.astype(float)
            # Adding a new column to store values later converted to the index of the results data frame
            res_df['sim_start_dates'] = 0
            # Adding enough rows
            new_rows = pd.DataFrame([[0] * len(res_df.columns)] * (len(sim_dates) - max_amt_factors), columns=res_df.columns)
            res_df = res_df._append(new_rows, ignore_index=True)

            # Changing the values in the new column to the simulation start dates
            res_df['sim_start_dates'] = sim_dates
            # Changing the sim_dates to the index
            res_df.set_index('sim_start_dates', inplace=True)

            # Setting the initial value of the return storing variable to 0
            ret = 0

            # Iterating over all end-of-LBP dates, which stand for the specific factor-portfolios created over the LBP up to that date
            for i in range(0, len(eom_dates)):
                # Storing the sorted factor names of the right column specified by the end of LBP date
                factor_names = fn_df[eom_dates[i]].tolist()

                # Iterating over all simulation periods
                for j in range(i, len(sim_dates)):
                    # Iterating over each of the previously selected highest performing factors over the LBP and storing its return in the simulation period
                    for k in range(0, z):
                        # return = sum of all factor returns for that month devided by the amount of factors
                        ret = ret + ret_df.at[factor_names[k], sim_dates[j]]

                    # Dividing the sum of the returns by the amount of factors invested per portfolio to get the equally weighted return
                    ret = ret / z
                    # STORING THE RETURN IN THE RESULTS DATA FRAME
                    res_df.iloc[j, i] = ret
                    ret = 0

            # EXPORTING THE RESULTING DATA FRAME!
            if export_type == 'csv':
                res_df.to_csv(f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv')
                print(f'CSV-file saved under name: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv')
            elif export_type == 'excel':
                res_df.to_excel(f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
                print(f'Excel-file saved under name: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
            elif export_type == 'both':
                res_df.to_csv(f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv')
                res_df.to_excel(f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
                print(
                    f'CSV- and Excel-files saved under names: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.format')
            else:
                print('Export file type wrong!!')
