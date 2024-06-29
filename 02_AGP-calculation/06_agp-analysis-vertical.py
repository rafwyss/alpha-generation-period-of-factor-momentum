import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
----------------------------------------------------------------------
Python-Script Nr. 6
**********************************************************************
DETERMINING THE ALPHA-GENERATION PERIOD (AGP)
(VERTICAL DATA FORMAT)
**********************************************************************
The amount of months, during which the factor momentum strategy still 
generated alpha is measured. Previously the trailing twelve months 
(TTM) returns of the factor momentum portfolios were calculated. The 
end of the alpha-generation period is now defined as the point in 
time, when TTM returns turn negative for the first time.
----------------------------------------------------------------------
The resulting AGP data is stored in a VERTICAL data frame (easier to 
conduct further analysis).
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

# This parameter sets the value stored, in case the first TTM return is already negative!
# The paper settles for 0.
less_than_12_months_value = 0


"""RESULTS DATA FRAME PREPARATION"""

# The following data is the basis for header row of the results data frame
results_data_frame_structure = {'eolbp': [],
                                'amount_of_factors': [],
                                'lbp_length': [],
                                'eras_long': [],
                                'eras_short': [],
                                'amount_of_months': [],
                                }
new_row_data = {'eolbp': '0', 'amount_of_factors': 0, 'lbp_length': 0, 'eras_long': '0', 'eras_short': '0', 'amount_of_months': 0, }


"""START OF THE ANALYSIS"""

# Iterating through all return weighting methods
for x in range(0, len(returns_weighting_list)):
    # Creating a results data frame, which is later appended with a new empty row during each iteration.
    res_df = pd.DataFrame(results_data_frame_structure)

    # Iterating over all percentiles
    for y in range(0, len(amt_factors_list)):
        # Iterating over all LBP-lengths
        for z in range(0, len(lbp_length_mths_list)):
            # Importing the corresponding TTM factor portfolio returns.
            ret_df = pd.read_csv(os.path.join('05_sim-ttm-pf-returns',
                f'sim_ttm_pf_returns_{returns_weighting_list[x]}_{lbp_length_mths_list[z]}mths_{amt_factors_list[y]}fctr.csv'))
            # Setting the indices to the simulation start dates
            ret_df.set_index('sim_start_dates', inplace=True)
            # Storing the Column headers and the indices in lists to iterate over later
            eolbp_dates = ret_df.columns.values.tolist()
            sim_dates = ret_df.index.values.tolist()

            # Iterating over all EOLBP dates of the specific file
            for i in range(0, len(eolbp_dates)):
                # Each EOLBP date represents one individual factor momentum strategy with a specific AGP
                # A new row is therefore added for each iteration
                res_df.loc[len(res_df)] = new_row_data

                # Next the EOLBP date can be added
                res_df.loc[len(res_df) - 1, 'eolbp'] = eolbp_dates[i]
                # Adding the length of the LBP
                res_df.loc[len(res_df) - 1, 'lbp_length'] = lbp_length_mths_list[z]
                # Adding the amount of factors
                res_df.loc[len(res_df) - 1, 'amount_of_factors'] = amt_factors_list[y]

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
                            res_df.loc[len(res_df) - 1, 'amount_of_months'] = less_than_12_months_value

                        # OBSERVABLE AGP:
                        # If the negative return didn't occur in the first sim period, the amount of months since
                        # inception (i.e. since the EOLBP date) is stored.
                        # Explanation: The amount of months is the 12 months from the TTM period plus the difference
                        # between j (month of first negative TTM-return) and i (EOLBP date) minus 1
                        else:
                            res_df.loc[len(res_df) - 1, 'amount_of_months'] = (j - i + 12 - 1)
                        # Breaking the loop after a result has been found.
                        break

                # NO NEGATIVE RETURN EVER OBSERVED
                # If no negative return is found throughout the entire simulation period up to 2023-12-31,
                # the total number of months after inception until 2023-12-31 is stored.
                # Alternatively, a string is stored, to showcase that the AGP never observably ended.
                else:
                    res_df.loc[len(res_df) - 1, 'amount_of_months'] = (len(sim_dates) - 1 - i + 12 - 1)
                    #res_df.loc[len(res_df) - 1, 'amount_of_months'] = 'FOREVER'

    """ERA CATEGORIZATION"""
    # The eolbp column is transformed into a datetime format.
    res_df['eolbp'] = pd.to_datetime(res_df['eolbp'])

    # 3 LONG ERAS of 15 years each
    # The correct eras are assigned.
    res_df.loc[res_df['eolbp'] <= '1990-12-31', 'eras_long'] = '1972-1990'
    res_df.loc[(res_df['eolbp'] > '1990-12-31') & (res_df['eolbp'] <= '2005-12-31'), 'eras_long'] = '1991-2005'
    res_df.loc[res_df['eolbp'] > '2005-12-31', 'eras_long'] = '2006-2021'

    # 8 SHORT ERAS of 5 years each
    # The correct eras are assigned.
    res_df.loc[res_df['eolbp'] <= '1985-12-31', 'eras_short'] = '1972-1985'
    res_df.loc[(res_df['eolbp'] > '1985-12-31') & (res_df['eolbp'] <= '1990-12-31'), 'eras_short'] = '1986-1990'
    res_df.loc[(res_df['eolbp'] > '1990-12-31') & (res_df['eolbp'] <= '1995-12-31'), 'eras_short'] = '1991-1995'
    res_df.loc[(res_df['eolbp'] > '1995-12-31') & (res_df['eolbp'] <= '2000-12-31'), 'eras_short'] = '1996-2000'
    res_df.loc[(res_df['eolbp'] > '2000-12-31') & (res_df['eolbp'] <= '2005-12-31'), 'eras_short'] = '2001-2005'
    res_df.loc[(res_df['eolbp'] > '2005-12-31') & (res_df['eolbp'] <= '2010-12-31'), 'eras_short'] = '2006-2010'
    res_df.loc[(res_df['eolbp'] > '2010-12-31') & (res_df['eolbp'] <= '2015-12-31'), 'eras_short'] = '2011-2015'
    res_df.loc[res_df['eolbp'] > '2015-12-31', 'eras_short'] = '2016-2021'

    # Exporting the resulting data frame!
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


# Creating a combined file
if len(returns_weighting_list) > 1:
    # Importing the relevant data.
    ew = pd.read_csv('agp_ew_vert.csv', index_col=0)
    ew['ret_w'] = 'ew'
    vw = pd.read_csv('agp_vw_vert.csv', index_col=0)
    vw['ret_w'] = 'vw'
    vw_cap = pd.read_csv('agp_vw_cap_vert.csv', index_col=0)
    vw_cap['ret_w'] = 'vw_cap'

    # Combining the data frames
    combined_res_df = pd.concat([ew, vw_cap, vw], axis=0)

    # Exporting the resulting data frame!
    if export_type == 'csv':
        combined_res_df.to_csv(f'agp_combined_vert.csv')
        print(f'CSV-file saved under name: agp_combined_vert.csv')
    elif export_type == 'excel':
        combined_res_df.to_excel(f'agp_combined_vert.xlsx')
        print(f'Excel-file saved under name: agp_combined_vert.xlsx')
    elif export_type == 'both':
        combined_res_df.to_csv(f'agp_combined_vert.csv')
        combined_res_df.to_excel(f'agp_combined_vert.xlsx')
        print(
            f'CSV- and Excel-files saved under names: agp_combined_vert.format')
    else:
        print('Export file type wrong!!')