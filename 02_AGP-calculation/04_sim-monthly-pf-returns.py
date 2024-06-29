import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 4
********************************************************************
CALCULATING THE MONTHLY FACTOR RETURNS OF THE SPECIFIED PORTFOLIO
OF FACTORS WITH THE HIGHEST PERFORMANCE OVER THE LOOK-BACK-PERIOD
********************************************************************
To generate the portfolios, the percentile of factors invested per 
factor momentum portfolio needs to be specified.
--------------------------------------------------------------------
153 Factors in Total. Options for amt_factors_list included in the 
paper:
Top Tercile = 51
Top Quintile: = 30
Top Decile:  = 15
Top 5%: 7
--------------------------------------------------------------------
The factor portfolio returns are calculated with an equally weighted 
return method, i.e with rebalancing at the beginning of every month.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'factors_sorted_for_total_factor_returns_{}_{}mths' FILE WITH SPECIFIED 
WEIGHTING METHOD AND LBP-LENGTH IN THE DIRECTORY, 
AS WELL AS A 'ret_{}_pivot.csv' FILE WITH SPECIFIED WEIGHTING METHOD IN THE '01-data-preparation' DIRECTORY"""

# Set equal to the amount of factors your factors_sorted_for_total_factor_returns....csv files contain
max_amt_factors = 51

# Specify the percentile (amount of factors)
amt_factors_list = [51, 30, 15, 7
                    ]

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Configure the weighting methods to your liking.
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lengths!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]


"""START OF THE ANALYSIS"""

# Iterating through all return weighting methods
for x in returns_weighting_list:
    # Iterating through all LBP lengths
    for y in lbp_length_mths_list:
        # Iterating through all percentiles
        for z in amt_factors_list:
            # Importing the relevant file containing the factor momentum portfolios with the sorted factor names (fn)
            fn_df = pd.read_csv(os.path.join('03_factors-ranked-by-total-factor-returns',f'factors_ranked_by_total_factor_returns_{x}_{y}mths.csv'), index_col=0)

            # Importing the factor returns pivot table file for the specified weighting scheme
            ret_df = pd.read_csv(os.path.join("..",'01_data-preparation', f'ret_{x}_pivot.csv'))
            ret_df.set_index('characteristic', inplace=True)

            # Storing the eom dates in a list
            eom_dates = fn_df.columns.values.tolist()

            # Making a new list containing the simulation period dates to work as the indexes.
            # The simulation dates are not equal to the end of LBP dates, because only looking at LBPs until 2021-12-31
            # are evaluated, while simulation period dates can be observed up until 2023-12-31.
            # Therefore, the sim_dates have to be obtained from a different source: the old return pivot table.
            sim_dates = ret_df.columns.values.tolist()
            # Deleting the simulation periods which lie prior to the earliest end of a LBP
            sim_dates = sim_dates[y:]


            # Preparing a data frame to store the results
            res_df = fn_df.copy()
            # Setting all values to 0
            res_df.iloc[0:, 0:] = 0
            # Changing the data type to floats, since the monthly pf returns are numerical.
            res_df = res_df.astype(float)
            # Adding a new column to store values later converted to the index of the results data frame
            res_df['sim_start_dates'] = 0
            # Calculating the right amount of rows in the results data frame
            new_rows = pd.DataFrame([[0] * len(res_df.columns)] * (len(sim_dates) - max_amt_factors), columns=res_df.columns)
            # Adding the new rows
            res_df = res_df._append(new_rows, ignore_index=True)

            # Changing the values in the new column to the simulation start dates
            res_df['sim_start_dates'] = sim_dates
            # Making the sim_dates the indices of the results data frame.
            res_df.set_index('sim_start_dates', inplace=True)

            # Setting the initial value of the return storing variable to 0
            ret = 0

            # Iterating over all end-of-LBP dates, which stand for the specific factor-portfolios created over the LBP up to that date
            for i in range(0, len(eom_dates)):
                # Storing the factor momentum portfolio in the right column specified by the end of LBP date
                factor_names = fn_df[eom_dates[i]].tolist()

                # Iterating over all simulation periods
                for j in range(i, len(sim_dates)):
                    # Iterating over the amount of factors per factor momentum portfolio
                    for k in range(0, z):
                        # Storing the sum of all monthly factor returns
                        # Explanation: return = sum of all factor returns for that month devided by  amount of factors
                        ret = ret + ret_df.at[factor_names[k], sim_dates[j]]

                    # Calculating the average return, i.e. monthly factor momentum portfolio return (equal weighting),
                    # by dividing the sum of monthly returns by the amount of factors invested per portfolio
                    ret = ret / z
                    # Storing the monthly factor momentum portfolio return in the return data frame
                    res_df.iloc[j, i] = ret
                    # Resetting the variable to 0 for the next iteration
                    ret = 0

            # Exporting the resulting data frame!
            if export_type == 'csv':
                res_df.to_csv(os.path.join('04_sim-monthly-pf-returns',f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv'))
                print(f'CSV-file saved under name: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv')
            elif export_type == 'excel':
                res_df.to_excel(os.path.join('04_sim-monthly-pf-returns',f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx'))
                print(f'Excel-file saved under name: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx')
            elif export_type == 'both':
                res_df.to_csv(os.path.join('04_sim-monthly-pf-returns',f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.csv'))
                res_df.to_excel(os.path.join('04_sim-monthly-pf-returns',f'sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.xlsx'))
                print(
                    f'CSV- and Excel-files saved under names: sim_monthly_pf_returns_{x}_{y}mths_{z}fctr.format')
            else:
                print('Export file type wrong!!')
