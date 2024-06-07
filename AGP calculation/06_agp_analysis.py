import pandas as pd
import numpy as np

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
----------------------------------------------------------------------
Python-Script Nr. 6
**********************************************************************
DETERMINING THE ALPHA-GENERATION PERIOD
**********************************************************************
In this file we analyse how many months the factor strategy still 
generated alpha. We previously calculated the trailing twelve months 
(TTM) returns of our factor portfolios. We define the end of the alpha-
generation period as the point in time, when TTM returns turn negative
for the first time.
----------------------------------------------------------------------
The resulting AGP data can be stored either in a pivot table format
(less data) or in a vertical data frame (easier to do further analysis).
"""

# Specify if you want the results stored in a pivot table format or in a vertical data frame.
# Options: 'pivot', 'vert'
results_structure = 'vert'

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
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

#IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR LBP-LENGTH IN THE DIRECTORY
# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

# OPTION PIVOT TABLE
if results_structure == 'pivot':
    # Preparing a new data frame to store the results.
    # The data frame should have the following structure.
    # Columns: end-of-LBP dates.
    # First row: Amount of months of positive returns (starting at 12)
    # We can use the data frame used for the TTM returns with the lowest LBP-length.
    res_df = pd.read_csv(
        f'sim_ttm_pf_returns_{returns_weighting_list[0]}_{lbp_length_mths_list[0]}mths_{amt_factors_list[0]}fctr.csv')
    # Setting all values in the results data frame to 0
    res_df.iloc[0:, 0:] = np.nan
    # We will need a varying amount of rows for all different combinations of LBP-length and amount of factors invested.
    amt_rows = len(lbp_length_mths_list) * len(amt_factors_list)
    res_df = res_df.iloc[0:amt_rows, 1:]
    res_df['identifier'] = ['0'] * amt_rows
    res_df['lbp_length'] = 0 * amt_rows
    res_df['amount_of_factors'] = 0 * amt_rows

    last_three_columns = res_df.iloc[:, -3:]
    remaining_columns = res_df.iloc[:, :-3]
    # Putting the last newly created columns at the start of the dataframe
    res_df = pd.concat([last_three_columns, remaining_columns], axis=1)


    # Filling the new columns with the specific identifier, lbp_length and amount of factors in the portfolios
    # Iterating over all different amounts of factors
    for i in range(0, len(amt_factors_list)):
        # Iterating over all different LBP-lengths
        for j in range(0, len(lbp_length_mths_list)):
            # Adding the identifier
            res_df.loc[j + i * len(
                lbp_length_mths_list), 'identifier'] = f'{lbp_length_mths_list[j]}_mths_{amt_factors_list[i]}_fctrs'
            # Adding the length of the LBP
            res_df.loc[j + i * len(lbp_length_mths_list), 'lbp_length'] = lbp_length_mths_list[j]
            # Adding the amount of factors
            res_df.loc[j + i * len(lbp_length_mths_list), 'amount_of_factors'] = amt_factors_list[i]
    # Making the identifier the index
    res_df.set_index('identifier', inplace=True)

    # START OF THE ANALYSIS
    print('PIVOT ANALYSIS STARTED')
    # Iterating over all returns weighting schemes
    for x in range(0, len(returns_weighting_list)):
        # Iterating over all LBP-lengths
        for y in range(0, len(lbp_length_mths_list)):
            # Iterating over all amounts of factors per portfolio
            for z in range(0, len(amt_factors_list)):
                # Importing the relevant file with the corresponding factor portfolio returns for each simulation period.
                ret_df = pd.read_csv(
                    f'sim_ttm_pf_returns_{returns_weighting_list[x]}_{lbp_length_mths_list[y]}mths_{amt_factors_list[z]}fctr.csv')
                # Making the Simulation Start dates the indices
                ret_df.set_index('sim_start_dates', inplace=True)
                # Storing the Column headers and the indices in lists to iterate over
                eolbp_dates = ret_df.columns.values.tolist()
                sim_dates = ret_df.index.values.tolist()

                # START OF THE ANALYSIS

                # We also need to decide which value we store if the first TTM return is already negative. I suggest assuming
                # that on average it would have worked for 6 months
                less_than_12_months_value = 0

                # Iterating over each end-of-LBP date
                for i in range(0, len(eolbp_dates)):
                    # Iterating over each simulation period date but always starting one period after the end-of-LBP date
                    for j in range(0, len(sim_dates)):
                        # If the TTM return is negative, we want to store the value of the amount of months leading up to that date.
                        if ret_df.iloc[j, i] < 0:
                            # If the first TTM return is already negative, this means the strategy never generated positive TTM-pf-returns
                            # We therefore store the value 6 to make it recognizable
                            if j == i:
                                res_df.iloc[(z * len(lbp_length_mths_list) + y), 2 + i + lbp_length_mths_list[
                                    y] - 12] = less_than_12_months_value
                            # If the negative return didn't happen in the first sim period, then we store the amount of months.
                            # The amount of months is the 12 months from the TTM period plus the difference between j and i
                            else:
                                res_df.iloc[
                                    (z * len(lbp_length_mths_list) + y), 2 + i + lbp_length_mths_list[y] - 12] = (
                                            j - i + 12 - 1)
                            # after we've found a negative return we want the for-loop to break and to continue with the next eolbp date
                            break
                    # If no negative return is found throughout the entire simulation period up to 2023-12-31
                    else:
                        res_df.iloc[(z * len(lbp_length_mths_list) + y), i + lbp_length_mths_list[y] - 12] = (
                                    len(sim_dates) - 1 - i + 12 - 1)

        # EXPORTING THE RESULTING DATA FRAME!
        if export_type == 'csv':
            res_df.to_csv(f'agp_{returns_weighting_list[x]}_pivot.csv')
            print(f'CSV-file saved under name: agp_{returns_weighting_list[x]}_pivot.csv')
        elif export_type == 'excel':
            res_df.to_excel(f'agp_{returns_weighting_list[x]}_pivot.xlsx')
            print(f'Excel-file saved under name: agp_{returns_weighting_list[x]}_pivot.xlsx')
        elif export_type == 'both':
            res_df.to_csv(f'agp_{returns_weighting_list[x]}_pivot.csv')
            res_df.to_excel(f'agp_{returns_weighting_list[x]}_pivot.xlsx')
            print(
                f'CSV- and Excel-files saved under names: agp_{returns_weighting_list[x]}_pivot.format')
        else:
            print('Export file type wrong!!')

# OPTION VERTICAL DATA FRAME
elif results_structure == 'vert':
    # We generate files for all three return weighting schemes

    # The following data is the basis for the results data frame
    results_data_frame_structure = {'eolbp': [],
                                    'amount_of_factors': [],
                                    'lbp_length': [],
                                    'amount_of_months': [],
                                    }
    new_row_data = {'eolbp': '0', 'amount_of_factors': 0, 'lbp_length': 0, 'amount_of_months': 0, }

    # We also need to decide which value we store if the first TTM return is already negative.
    less_than_12_months_value = 0

    print('VERT ANALYSIS STARTED')
    # Iterating over all returns weighting schemes
    for x in range(0, len(returns_weighting_list)):

        # Create a new data frame to store the results in. The data frame will be appended with a new empty row with each iteration.

        res_df = pd.DataFrame(results_data_frame_structure)

        # Iterating over all amounts of factors per portfolio
        for y in range(0, len(amt_factors_list)):
            # Iterating over all LBP-lengths
            for z in range(0, len(lbp_length_mths_list)):
                # First we import the correct sim_ttm_pf_returns... file
                ret_df = pd.read_csv(
                    f'sim_ttm_pf_returns_{returns_weighting_list[x]}_{lbp_length_mths_list[z]}mths_{amt_factors_list[y]}fctr.csv')
                # Making the Simulation Start dates the indices
                ret_df.set_index('sim_start_dates', inplace=True)
                # Storing the Column headers and the indices in lists to iterate over
                eolbp_dates = ret_df.columns.values.tolist()
                sim_dates = ret_df.index.values.tolist()

                # Then we iterate over all EOLBP dates of the specific file
                for i in range(0, len(eolbp_dates)):
                    # Each EOLBP date represents one specific investment strategy with a specific AGP
                    #  A new row is therefore added for each iteration
                    res_df.loc[len(res_df)] = new_row_data

                    # Next the EOLBP date can be added
                    res_df.loc[len(res_df) - 1, 'eolbp'] = eolbp_dates[i]
                    # Adding the length of the LBP
                    res_df.loc[len(res_df) - 1, 'lbp_length'] = lbp_length_mths_list[z]
                    # Adding the amount of factors
                    res_df.loc[len(res_df) - 1, 'amount_of_factors'] = amt_factors_list[y]

                    # Iterating over each simulation period date but always starting one period after the end-of-LBP date
                    for j in range(0, len(sim_dates)):
                        # If the TTM return is negative, we want to store the value of the amount of months leading up to that date.
                        if ret_df.iloc[j, i] < 0:
                            # If the first TTM return is already negative, this means the strategy never generated positive TTM-pf-returns
                            # We therefore store the value 6 to make it recognizable
                            if j == i:
                                res_df.loc[len(res_df) - 1, 'amount_of_months'] = less_than_12_months_value
                            # If the negative return didn't happen in the first sim period, then we store the amount of months.
                            # The amount of months is the 12 months from the TTM period plus the difference between j and i
                            else:
                                res_df.loc[len(res_df) - 1, 'amount_of_months'] = (j - i + 12 - 1)
                            # after we've found a negative return we want the for-loop to break and to continue with the next eolbp date
                            break
                    # If no negative return is found throughout the entire simulation period up to 2023-12-31
                    else:
                        res_df.loc[len(res_df) - 1, 'amount_of_months'] = (len(sim_dates) - 1 - i + 12 - 1)

        # EXPORTING THE RESULTING DATA FRAME!
        if export_type == 'csv':
            res_df.to_csv(f'agp_{returns_weighting_list[x]}_vert.csv')
            print(f'CSV-file saved under name: agp_{returns_weighting_list[x]}_vert.csv')
        elif export_type == 'excel':
            res_df.to_excel(f'agp_{returns_weighting_list[x]}_vert.xlsx')
            print(f'Excel-file saved under name: agp_{returns_weighting_list[x]}_vert.xlsx')
        elif export_type == 'both':
            res_df.to_csv(f'agp_{returns_weighting_list[x]}_vert.csv')
            res_df.to_excel(f'agp_{returns_weighting_list[x]}_vert.xlsx')
            print(
                f'CSV- and Excel-files saved under names: agp_{returns_weighting_list[x]}_vert.format')
        else:
            print('Export file type wrong!!')
else:
    print('#PIVOT/VERT ERROR')
