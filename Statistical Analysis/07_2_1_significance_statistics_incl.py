import pandas as pd
import scipy.stats as stats
import math

"""
CREATING SUMMARY STATISTICS FOR ALL DIFFERENT VARIABLE COMBINATIONS
INCLUDING BELOW 13 MONTHS AGPs!!!
"""


amt_factors_list = [51,
                    30, 15, 7
                    ]

# Decide in which format you want the dataframe exported!
# Possible Options: 'csv', 'excel' or 'both'
export_type = 'csv'

# Please configure the weighting schemes to your liking.
# IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR SPECIFIED WEIGHTING SCHEME IN THE DIRECTORY
# possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = ['ew',
                          'vw', 'vw_cap'
                          ]

#IMPORTANT: THIS CODE ONLY WORKS IF THERE IS A FULL_LBP_RET FILE WITH YOUR LBP-LENGTH IN THE DIRECTORY
# Specify all Look-back-period lenghts over which you want to have the total factor returns computed!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]


# DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
column_list = ['identifier','ret_weighting', 'amount_of_factors', 'lbp_length', 'mean', 'std', 'CI_bottom', 'CI_top', 't_stat', 'p_value']

# The data frame to store the results is created
summary_stats = pd.DataFrame(columns=column_list, index=[0])
summary_stats.iloc[0, :] = 0

# Filling the new columns with the specific identifier, lbp_length and amount of factors in the portfolios
# Iterating over all different amounts of factors
len_lbp = len(lbp_length_mths_list)
len_fctrs = len(amt_factors_list)

"""
# TESTING
df = pd.read_csv(f'agp_{returns_weighting_list[0]}_vert.csv', index_col=0)

# HYPOTHESIS TESTING
t_test = stats.ttest_1samp(a = df.loc[(df['amount_of_factors'] == amt_factors_list[0]) & (df['lbp_length'] == lbp_length_mths_list[0]), ['amount_of_months']],
                           popmean = 24)

print(t_test)
"""

for i in range(0,len(returns_weighting_list)):
    df = pd.read_csv(f'agp_{returns_weighting_list[i]}_vert.csv', index_col=0)

    for j in range(0, len(amt_factors_list)):
        # Iterating over all different LBP-lengths
        for k in range(0, len(lbp_length_mths_list)):
            # Adding the identifier
            summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{amt_factors_list[j]}_fctrs'
            # Adding the return weighting scheme
            summary_stats.loc[k + j * len_lbp + i * len_lbp * len_fctrs, 'ret_weighting'] = returns_weighting_list[i]
            # Adding the length of the LBP
            summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, 'lbp_length'] = lbp_length_mths_list[k]
            # Adding the amount of factors
            summary_stats.loc[k + j * len_lbp+ i * len_lbp*len_fctrs, 'amount_of_factors'] = amt_factors_list[j]

            total_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k])).sum()


            # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
            describe = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]), ['amount_of_months']].describe()
            descr = describe.loc[['mean', 'std']]

            # CONFIDENCE INTERVAL
            ci_interval = stats.t.interval(confidence = 0.05,
                                   df = total_count-1,
                                   loc =  descr.loc['mean', 'amount_of_months'],
                                   scale = descr.loc['std', 'amount_of_months'])

            descr.loc['CI_bottom'] = ci_interval[0]
            descr.loc['CI_top'] = ci_interval[1]

            # HYPOTHESIS TESTING
            t_test = stats.ttest_1samp(a = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]), ['amount_of_months']],
                                       popmean = 24,
                                       alternative = 'greater')

            descr.loc['t_stat'] = t_test[0][0]
            descr.loc['p_value'] = t_test[1][0]

            # Assigning the values to the summary_stats data frame
            for x in column_list[4:]:
                summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, x] = descr.loc[x, 'amount_of_months']
print(summary_stats)

summary_stats.to_csv('agp_significance_statistics_incl.csv')
print(f'CSV-File exported under the name: agp_significance_statistics_incl.csv')
"""
"""