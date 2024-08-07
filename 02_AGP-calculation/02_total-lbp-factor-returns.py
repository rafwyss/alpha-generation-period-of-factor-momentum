import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Python-Script Nr. 2
********************************************************************
CALCULATION OF TOTAL FACTOR RETURNS OVER THE ENTIRE LOOK-BACK PERIOD
FOR ALL FACTORS FROM DIFFERENT STARTING POINTS IN TIME
********************************************************************
This file automatically computes all total, compounded factor returns
over the entire LBP for all factors over different time frames.
--------------------------------------------------------------------
To run the program first specify all the different LBP lengths and
returns_weighting schemes over which you want to run the program and
create the total factor returns.
--------------------------------------------------------------------
"""

""" IMPORTANT: CODE ONLY WORKS IF THERE IS A 'ret_{}_pivot.csv' FILE WITH SPECIFIED WEIGHTING METHOD 
IN THE '01-data-preparation' DIRECTORY"""

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Specify all return weighting methods!
# IF YOU ONLY WANT ONE TYPE OF RETURN WEIGHTING, DELETE THE OTHERS OUT OF THE LIST!!!
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lengths over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

""" START OF THE ANALYSIS PROGRAM"""

# One iteration of the entire code will generate one file with the total factor returns over the entire LBP.
# To get all the data-files we want, we run the program over all specified return weighting schemes and all specified LBP-lengths

# Iterating over all return weighting methods
for x in range(0, len(returns_weighting_list)):
    # Setting the returns weighting method
    returns_weighting = returns_weighting_list[x]
    # Iterating over all LBP-lengths
    for y in range(0, len(lbp_length_mths_list)):
        # Setting the LBP-length
        lbp_length_mths = lbp_length_mths_list[y]

        # Importing the previously prepared CSV-file with the corresponding factor returns
        df = pd.read_csv(os.path.join("..",'01_data-preparation', f'ret_{returns_weighting}_pivot.csv'))

        # Making the factor_names the indices of the main dataframe
        df.set_index('characteristic', inplace=True)

        # Creating a new dataframe to store the total factor returns under the correct indices standing for the end of the LBP
        res_df = df.copy()

        # Saving the factor names to a list
        eom_date = df.columns.values.tolist()

        # Deleting the first item in the list, as it is the header 'characteristics' and not an eom_date
        # Saving the eom dates from the indices to a list
        factor_names = df.index.tolist()

        # Dropping all irrelevant columns, so that the structure of new_df suits the results perfectly.
        for i in eom_date:
            # The results should be stored in a dataframe with the headers of the columns equaling the end of its
            # respective lbp. Therefore: any columns where the header (eom_date) is at least the LBP-length amount of
            # months away from the starting date( 1980-01-31). The resulting dataframe's first column
            # is always the end of the lbp of the earliest LBP.
            if i >= eom_date[lbp_length_mths - 1] and i <= '2021-12-31':
                # Nothing is done
                ()
            else:
                # The column is dropped.
                res_df = res_df.drop(columns=[i])

        # Calculating the total amount of timeframes analysed
        total_number_of_timeframes = len(eom_date)
        number_of_timeframes_after_2021 = 24
        # Printing the eom_date with the following index should result with the last wanted date: 2021-12-31
        #print(eom_date[total_number_of_timeframes-number_of_timeframes_after_2021])
        # Secondly it has to be considered that over the initial LBP length there will also be no results
        # The amount of timeframes is therefore further adjusted
        amt_timeframes = total_number_of_timeframes - number_of_timeframes_after_2021 - lbp_length_mths

        # The amount of different factors is equal to the amount of elements in the list 'factor_names', which is 153
        amt_factors = len(factor_names)

        # Creating the storage variable for the full lbp return and setting it to 1
        full_lbp_geom_ret = 1

        # Iterating over all factor names
        for i in range(0, amt_factors):
            # Iterating over all analysed timeframes
            for j in range(0, amt_timeframes):
                # Iterating over all periods in the LBP.
                for k in range(0, lbp_length_mths):
                    # The total GEOMETRIC factor return over the LBP is iteratively achieved by multiplying the previous
                    # result by (1 + the return of next period)
                    # Explanation: df.loc[eom_date[k+i], factor_names[j]] is the factor return;
                    # Example: df.loc[eom_date[0], factor_names[0]] is the return of the factor age on 1980-01-31
                    full_lbp_geom_ret = full_lbp_geom_ret * (1 + df.loc[factor_names[i], eom_date[k + j]])
                # The achieved full factor return is stored in the previously prepared dataframe res_df
                # The index of the first row of res_df is 1989-12-31, which is the end of the LBP of the first iteration
                res_df.iloc[i, j] = full_lbp_geom_ret - 1
                # The variable storing the full factor return is reset to 1 for the iterations on the next timeframe
                full_lbp_geom_ret = 1

        # Exporting the resulting data frame!
        if export_type == 'csv':
            res_df.to_csv(os.path.join('02_total-LBP-factor-returns', f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv'))
            print(f'CSV-file saved under name: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv')
        elif export_type == 'excel':
            res_df.to_excel(os.path.join('02_total-LBP-factor-returns', f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx'))
            print(f'Excel-file saved under name: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx')
        elif export_type == 'both':
            res_df.to_csv(os.path.join('02_total-LBP-factor-returns', f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv'))
            res_df.to_excel(os.path.join('02_total-LBP-factor-returns', f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx'))
            print(
                f'CSV- and Excel-files saved under names: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.format')
        else:
            print('Export file type wrong!!')