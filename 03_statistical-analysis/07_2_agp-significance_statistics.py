import pandas as pd
import scipy.stats as stats
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.2
********************************************************************
SIGNIFICANCE STATISTICS FOR ALL DIFFERENT VARIABLE COMBINATIONS
********************************************************************
Significance statistics are generated for all return weighting 
methods together in one single file.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED 
WEIGHTING METHOD, AND INCLUDING THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the percentile (amount of factors)
amt_factors_list = [51,
                    30, 15, 7
                    ]

# Please configure the weighting schemes to your liking.
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting_list = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Specify all Look-back-period lengths!
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

# Statistical measures are defined.
column_list = ['identifier','ret_weighting', 'amount_of_factors', 'lbp_length', 'mean', 'std', 't_stat', 'p_value', 'CI_bottom', 'CI_top',]

# The data frame to store the results is created
summary_stats = pd.DataFrame(columns=column_list, index=[0])
summary_stats.iloc[0, :] = 0


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

            total_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k])).sum()


            """CREATING THE SIGNIFICANCE STATISTICS"""
            # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
            describe = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]), ['amount_of_months']].describe()
            descr = describe.loc[['mean', 'std']]

            # HYPOTHESIS TESTING
            t_test = stats.ttest_1samp(a=df.loc[
                (df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]), [
                    'amount_of_months']],
                                       popmean=24,
                                       alternative='greater')
            # Storing the results
            descr.loc['t_stat'] = t_test[0][0]
            descr.loc['p_value'] = t_test[1][0]


            # CONFIDENCE INTERVAL
            ci_interval = stats.t.interval(confidence = 0.05,
                                   df = total_count-1,
                                   loc =  descr.loc['mean', 'amount_of_months'],
                                   scale = descr.loc['std', 'amount_of_months'])
            # Storing the results
            descr.loc['CI_bottom'] = ci_interval[0]
            descr.loc['CI_top'] = ci_interval[1]


            # Adding the significance results into the results data frame.
            for x in column_list[4:]:
                summary_stats.loc[k + j * len_lbp + i * len_lbp*len_fctrs, x] = descr.loc[x, 'amount_of_months']

# Exporting the results as a CSV file.
summary_stats.to_csv(os.path.join('07_statistics','agp_significance_statistics_incl.csv'))
print(f'CSV-File exported under the name: agp_significance_statistics_incl.csv')