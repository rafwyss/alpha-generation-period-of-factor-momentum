import pandas as pd

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
# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Specify all return weighting schemes!
""" IF YOU ONLY WANT ONE TYPE OF RETURN WEIGHTING, DELETE THE OTHERS OUT OF THE LIST!!!"""
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

""" START OF THE ANALYSIS PROGRAM"""

# One iteration of the entire code will generate one file with the correct total factor returns.
# To get all the data-files we want, we run the program over all specified return weighting schemes and
# all specified LBP-lengths

for x in range(0, len(returns_weighting_list)):
    # setting the returns weighting scheme
    returns_weighting = returns_weighting_list[x]

    for y in range(0, len(lbp_length_mths_list)):
        # setting the LBP-length
        lbp_length_mths = lbp_length_mths_list[y]

        # Importing the previously prepared CSV-file with the corresponding factor returns
        df = pd.read_csv(f'ret_{returns_weighting}_pivot.csv')

        # Making the factor_names the indices of the main dataframe
        df.set_index('characteristic', inplace=True)

        # Creating a new dataframe to store the total factor returns under the correct indices standing for the end of the LBP
        res_df = df.copy()

        # saving the factor names to a list
        eom_date = df.columns.values.tolist()

        # Deleting the first item in the list, as it is the header 'characteristics' and not an eom_date
        # saving the eom dates from the indices to a list
        factor_names = df.index.tolist()

        # Dropping all irrelevant columns, so that the structure of new_df suits the results perfectly.
        for i in eom_date:
            #We want to store the results in a dataframe with the headers of the columns equaling the end of its
            # respective lbp. Therefore: any columns where the header (eom_date) is at least the LBP-length amount of
            # months away from the starting date( 1980-01-31), then we keep it. The resulting dataframe's first column
            # is always the end of the lbp of the earliest LBP.
            if i >= eom_date[lbp_length_mths - 1] and i <= '2021-12-31':
                ()
            else:
                res_df = res_df.drop(columns=[i])

        # eom_date[0] = 1971-11-30
        # factor_names[0] = age

        # Calculating the total amount of timeframes analysed
        # there are total of 625 eom dates, however we only want them up until 2021-12-31, which is the 25th last eom date
        # print(eom_date[503])

        # secondly we have to consider that over the initial period of the length of the lbp there will also be no results
        # the amount of timeframes will be equal to 625-24 minus the length of the lbp in months
        amt_timeframes = 625-24 - lbp_length_mths
        # the amount of different factors is equal to the amount of elements in the list 'factor_names', which is 153
        amt_factors = len(factor_names)

        # Creating the storage variable for the full lbp return and setting it to 1
        full_lbp_geom_ret = 1

        # Iterate through all factor names
        for i in range(0, amt_factors):
            # Iterate through all analysed timeframes
            for j in range(0, amt_timeframes):
                # Iterating through all the periods in the LBP.
                for k in range(0, lbp_length_mths):
                    # The full factor return over the LBP is slowly achieved by multiplying it by (1 + the return of next period)
                    # df.loc[eom_date[k+i], factor_names[j]] is the factor return;
                    # df.loc[eom_date[0], factor_names[0]] is the return of the factor age on 1980-01-31
                    full_lbp_geom_ret = full_lbp_geom_ret * (1 + df.loc[factor_names[i], eom_date[k + j]])
                # The achieved full factor return is stored in the previously prepared dataframe new_df
                # the index of the first row of new_df is 1989-12-31, which is the end of the LBP of the first iteration
                res_df.iloc[i, j] = full_lbp_geom_ret - 1
                # the variable storing the full factor return is reset to 1 for the iterations on the next timeframe
                full_lbp_geom_ret = 1


        if export_type == 'csv':
            res_df.to_csv(f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv')
            print(f'CSV-file saved under name: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv')
        elif export_type == 'excel':
            res_df.to_excel(f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx')
            print(f'Excel-file saved under name: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx')
        elif export_type == 'both':
            res_df.to_csv(f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.csv')
            res_df.to_excel(f'total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.xlsx')
            print(
                f'CSV- and Excel-files saved under names: total_lbp_ret_{returns_weighting}_{lbp_length_mths}mths.format')
        else:
            print('Export file type wrong!!')
