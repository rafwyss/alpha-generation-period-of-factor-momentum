import pandas as pd
import numpy as np
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
----------------------------------------------------------------------
Additional Python-Script Nr. 6a
**********************************************************************
DETERMINING THE ALPHA-GENERATION PERIOD (AGP)
(PIVOT TABLE DATA FORMAT)
**********************************************************************
The amount of months, during which the factor momentum strategy still 
generated alpha is measured. Previously the trailing twelve months 
(TTM) returns of the factor momentum portfolios were calculated. The 
end of the alpha-generation period is now defined as the point in 
time, when TTM returns turn negative for the first time.
----------------------------------------------------------------------
The resulting AGP data is stored in a PIVOT TABLE data frame (easier 
to read and great for Excel analysis).
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'sim_ttm_pf_returns_{}_{}mths_{}fctr.csv' FILE WITH THE SPECIFIED 
WEIGHTING METHOD, LBP-LENGTH AND AMOUNT OF FACTORS IN THE DIRECTORY"""

# Specify the percentile (amount of factors)
amt_factors_list = [51,
                    30, 15, 7
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
shortest_lbp = min(lbp_length_mths_list)

# This parameter sets the value stored, in case the first TTM return is already negative!
# The paper settles for 0.
less_than_12_months_value = 0


"""RESULTS DATA FRAME PREPARATION"""

# The results data frame should have the following structure:
    # Columns: end-of-LBP dates.
    # First row: Amount of months of positive returns (starting at 12)

# For this purpose, the data frame containing TTM returns with the lowest LBP-length can be used.
res_df = pd.read_csv(os.path.join('05_sim-ttm-pf-returns',
    f'sim_ttm_pf_returns_{returns_weighting_list[0]}_{lbp_length_mths_list[0]}mths_{amt_factors_list[0]}fctr.csv'))

# Setting all values in the results data frame to 0
res_df.iloc[0:, 0:] = np.nan

# This file shall be able to accommodate a varying amount of rows for all different combinations of LBP-length and
# amount of factors invested.
# Amount of rows: Amount of individual combinations of LBP-lengths and percentiles
amt_rows = len(lbp_length_mths_list) * len(amt_factors_list)

# Creating the new rows to store the results in.
res_df = res_df.iloc[0:amt_rows, 1:]

# Adding descriptive columns for an identifier, the LBP-length and the percentile (amount of factors)
res_df['identifier'] = ['0'] * amt_rows
res_df['lbp_length'] = 0 * amt_rows
res_df['amount_of_factors'] = 0 * amt_rows

last_three_columns = res_df.iloc[:, -3:]
remaining_columns = res_df.iloc[:, :-3]
# Moving the descriptive columns to the front (left).
res_df = pd.concat([last_three_columns, remaining_columns], axis=1)


# Filling the descriptive columns with the specific identifier, lbp_length and amount of factors in the portfolios
# Iterating over all percentiles
for i in range(0, len(amt_factors_list)):
    # Iterating over all different LBP-lengths
    for j in range(0, len(lbp_length_mths_list)):
        # Adding the identifier
        res_df.loc[j + i * len(
            lbp_length_mths_list), 'identifier'] = f'{lbp_length_mths_list[j]}_mths_{amt_factors_list[i]}_fctrs'
        # Adding the length of the LBP
        res_df.loc[j + i * len(lbp_length_mths_list), 'lbp_length'] = lbp_length_mths_list[j]
        # Adding the percentile (amount of factors)
        res_df.loc[j + i * len(lbp_length_mths_list), 'amount_of_factors'] = amt_factors_list[i]
# Making the identifier the index
res_df.set_index('identifier', inplace=True)


"""START OF THE ANALYSIS"""

# Iterating over all return weighting methods
for x in range(0, len(returns_weighting_list)):
    # Iterating over all LBP-lengths
    for y in range(0, len(lbp_length_mths_list)):
        # Iterating over all amounts of factors per portfolio
        for z in range(0, len(amt_factors_list)):
            # Importing the corresponding TTM factor portfolio returns.
            ret_df = pd.read_csv(os.path.join('05_sim-ttm-pf-returns',
                f'sim_ttm_pf_returns_{returns_weighting_list[x]}_{lbp_length_mths_list[y]}mths_{amt_factors_list[z]}fctr.csv'))
            # Setting the indices to the simulation start dates
            ret_df.set_index('sim_start_dates', inplace=True)
            # Storing the Column headers and the indices in lists to iterate over
            eolbp_dates = ret_df.columns.values.tolist()
            sim_dates = ret_df.index.values.tolist()

            # Iterating over each end-of-LBP date
            for i in range(0, len(eolbp_dates)):
                # Iterating over each simulation period date but always starting one period after the end-of-LBP date
                for j in range(0, len(sim_dates)):
                    # NEGATIVE TTM-RETURN OBSERVABLE
                    # If the TTM return is negative, the AGP has ended and the duration of the AGP is measured.
                    if ret_df.iloc[j, i] < 0:
                        # NO OBSERVABLE AGP:
                        # If the first observable TTM return (12 months after the inception of the FM portfolio), is
                        # already negative, the strategy never generated positive TTM-pf-returns.
                        # Therefore, the value for this scenario specified above (less_than_12_months_value) is stored.
                        if j == i:
                            res_df.iloc[(z * len(lbp_length_mths_list) + y), 2 + i + lbp_length_mths_list[
                                y] - shortest_lbp] = less_than_12_months_value

                        # OBSERVABLE AGP:
                        # If the negative return didn't occur in the first sim period, the amount of months since
                        # inception (i.e. since the EOLBP date) is stored.
                        # Explanation: The amount of months is the 12 months from the TTM period plus the difference
                        # between j (month of first negative TTM-return) and i (EOLBP date) minus 1
                        else:
                            res_df.iloc[
                                (z * len(lbp_length_mths_list) + y), 2 + i + lbp_length_mths_list[y] - shortest_lbp] = (
                                        j - i + 12 - 1)
                        # Breaking the loop after a result has been found.
                        break

                # NO NEGATIVE RETURN EVER OBSERVED
                # If no negative return is found throughout the entire simulation period up to 2023-12-31,
                # the total number of months after inception until 2023-12-31 is stored.
                # Alternatively, a string is stored, to showcase that the AGP never observably ended.
                else:
                    res_df.iloc[(z * len(lbp_length_mths_list) + y), i + lbp_length_mths_list[y] - shortest_lbp] = (len(sim_dates) - 1 - i + 12 - 1)
                    #res_df.iloc[(z * len(lbp_length_mths_list) + y), i + lbp_length_mths_list[y] - shortest_lbp] = 'FOREVER'

    # Exporting the resulting data frame!
    if export_type == 'csv':
        res_df.to_csv(os.path.join('06a_agp_pivot',f'agp_{returns_weighting_list[x]}_pivot.csv'))
        print(f'CSV-file saved under name: agp_{returns_weighting_list[x]}_pivot.csv')
    elif export_type == 'excel':
        res_df.to_excel(os.path.join('06a_agp_pivot',f'agp_{returns_weighting_list[x]}_pivot.xlsx'))
        print(f'Excel-file saved under name: agp_{returns_weighting_list[x]}_pivot.xlsx')
    elif export_type == 'both':
        res_df.to_csv(os.path.join('06a_agp_pivot',f'agp_{returns_weighting_list[x]}_pivot.csv'))
        res_df.to_excel(os.path.join('06a_agp_pivot',f'agp_{returns_weighting_list[x]}_pivot.xlsx'))
        print(
            f'CSV- and Excel-files saved under names: agp_{returns_weighting_list[x]}_pivot.format')
    else:
        print('Export file type wrong!!')