import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.1a
********************************************************************
SUMMARY STATISTICS FOR ALL DIFFERENT VARIABLE COMBINATIONS
(excluding results where no AGP was ever observed)
********************************************************************
Results, where no AGP was ever observed (i.e. where the AGP is 0), 
are excluded from the data analysed. AGP summary statistics are 
therefore calculated under the condition, that the first TTM-return 
was positive. Additionally, the percentage of APGs of at least 12 
months and shorter than 12 months is computed. Summary statistics 
are generated for all return weighting methods together in one single 
file. 
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED 
WEIGHTING METHOD, AND INCLUDING THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""


# Specify the percentile (amount of factors)
amt_factors_list = [51,
                    30, 15, 7
                    ]

# Configure the weighting schemes to your liking.
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lengths!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]


"""RESULTS DATA FRAME PREPARATION"""
# DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
column_list = ['identifier','ret_weighting', 'amount_of_factors', 'lbp_length', 'percent_under_12_months', 'percent_12_months_or_over', 'percent_under_24_months', 'percent_24_months_or_over', 'mean', 'median', 'std', 'var', 'min', '25%', '50%', '75%', 'max', 'skew',
             'kurt', 'count']

# The data frame to store the results is created
summary_stats = pd.DataFrame(columns=column_list, index=[0])
summary_stats.iloc[0, :] = 0


# Iterating over all different amounts of factors
len_lbp = len(lbp_length_mths_list)
len_fctrs = len(amt_factors_list)

# Iterating over all return weighting methods
for i in range(0,len(returns_weighting_list)):
    # Importing the corresponding AGP results data
    df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{returns_weighting_list[i]}_vert.csv'), index_col=0)
    # Iterating over all percentiles
    for j in range(0, len(amt_factors_list)):
        # Iterating over all different LBP-lengths
        for k in range(0, len(lbp_length_mths_list)):
            # Filling the new columns with the specific identifier, lbp_length and amount of factors in the portfolios
            # Adding the identifier
            summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{amt_factors_list[j]}_fctrs'
            # Adding the return weighting scheme
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'ret_weighting'] = returns_weighting_list[i]
            # Adding the length of the LBP
            summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, 'lbp_length'] = lbp_length_mths_list[k]
            # Adding the amount of factors
            summary_stats.loc[k + j * len_lbp+ i * len_lbp*len_fctrs, 'amount_of_factors'] = amt_factors_list[j]

            """CREATING THE STATISTICAL METRICS YOU ADDED INTO THE COLUMN LIST ABOVE"""
            # Calculating the percentages under and over 12 months
            total_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k])).sum()
            under_12months_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] < 12)).sum()
            under_24months_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] < 24)).sum()

            # Adding the percentages under and over 13 months to the summary statistics table
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'percent_under_12_months'] = (under_12months_count / total_count)
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'percent_12_months_or_over'] =1 - (under_12months_count / total_count)

            # Adding the percentages under and over 13 months to the summary statistics table
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'percent_under_24_months'] = (under_24months_count / total_count)
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'percent_24_months_or_over'] = 1- (under_24months_count / total_count)

            # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
            descr = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] > 12), ['amount_of_months']].describe()
            descr.loc['median'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] > 12), ['amount_of_months']].median()
            descr.loc['var'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] > 12), ['amount_of_months']].var()
            descr.loc['skew'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] > 12), ['amount_of_months']].skew()
            descr.loc['kurt'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['amount_of_months'] > 12), ['amount_of_months']].kurt()

            # Adding the statistical measures into the results data frame.
            for x in column_list[8:]:
                summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, x] = descr.loc[x, 'amount_of_months']

# Exporting the summary statistics as a CSV file.
summary_stats.to_csv(os.path.join('07_statistics','agp_summary_statistics_excl.csv'))
print(f'CSV-File exported under the name: agp_summary_statistics_excl.csv')
