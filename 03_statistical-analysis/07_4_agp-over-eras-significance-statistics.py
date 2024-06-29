import pandas as pd
import scipy.stats as stats
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.4
********************************************************************
SIGNIFICANCE STATISTICS FOR ALL DIFFERENT VARIABLE COMBINATIONS OVER 
MULTIPLE ERAS
********************************************************************
This file allows the computation of significance statistics for two 
different era lengths: 15 years or 5 years. 
Significance statistics are generated for all return weighting 
methods together in one single file.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""


# Specify the length of the era you want!
# Options: For 3 eras à 15 years: 'eras_long'. For 8 eras à 5 years: 'eras_short'.
eras_length = 'eras_long'

eras = []
if eras_length == 'eras_long':
    eras = ['1972-1990', '1991-2005', '2006-2021']
elif eras_length == 'eras_short':
    eras =['1972-1985', '1986-1990', '1991-1995', '1996-2000', '2001-2005', '2006-2010', '2011-2015', '2016-2021']

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
lbp_length_mths_list = [#12,
                        #24, 36, 48, 60, 72, 84, 96,
                        108, 120
                        ]

# The data frame to store the results is created
# DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
column_list = ['identifier', 'era','ret_weighting', 'amount_of_factors', 'lbp_length', 'mean', 'median', 'std', 'CI_bottom', 'CI_top', 't_stat', 'p_value']
significance_stats = pd.DataFrame(columns=column_list, index=[0])

len_lbp = len(lbp_length_mths_list)
len_fctrs = len(amt_factors_list)
len_eras = len(eras)

# Iterating over all return weighting methods
for i in range(0,len(returns_weighting_list)):
    # Importing the corresponding AGP results data
    df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{returns_weighting_list[i]}_vert.csv'), index_col=0)
    # Iterating over all percentiles
    for j in range(0, len(amt_factors_list)):
        # Iterating over all different LBP-lengths
        for k in range(0, len(lbp_length_mths_list)):
            # Iterating over all eras
            for e in range(0, len(eras)):
                # Filling the new columns with the specific identifier, lbp_length and amount of factors in the portfolios
                # Adding the identifier
                significance_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{amt_factors_list[j]}_fctrs_{eras[e]}'
                # Adding the era
                significance_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'era'] = eras[e]
                # Adding the return weighting scheme
                significance_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'ret_weighting'] = returns_weighting_list[i]
                # Adding the length of the LBP
                significance_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'lbp_length'] = lbp_length_mths_list[k]
                # Adding the amount of factors
                significance_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'amount_of_factors'] = amt_factors_list[j]

                # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
                describe = df.loc[
                    (df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (
                                df[f'{eras_length}'] == eras[e]), ['amount_of_months']].describe()
                descr = describe.loc[['mean', '50%', 'std']]
                descr.rename(index={'50%': 'median'}, inplace=True)

               # Getting the amount of results, which is relevant for the degrees of freedom.
                total_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (
                            df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{eras_length}'] == eras[e])).sum()

                # HYPOTHESIS TESTING
                t_test = stats.ttest_1samp(a=df.loc[
                    (df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (
                                df[f'{eras_length}'] == eras[e]), ['amount_of_months']], popmean=24, alternative='greater')
                # Storing the results
                descr.loc['t_stat'] = t_test[0][0]
                descr.loc['p_value'] = t_test[1][0]


                # CONFIDENCE INTERVAL
                ci_interval = stats.t.interval(confidence=0.05,
                                               df=total_count - 1,
                                               loc=descr.loc['mean', 'amount_of_months'],
                                               scale=descr.loc['std', 'amount_of_months'])
                # Storing the results
                descr.loc['CI_bottom'] = ci_interval[0]
                descr.loc['CI_top'] = ci_interval[1]


                # Adding the statistical measures into the results data frame.
                for x in column_list[5:]:
                    significance_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs *len_eras, x] = descr.loc[x, 'amount_of_months']

# Exporting the results as a CSV file.
significance_stats.to_csv(os.path.join('07_statistics',f'agp_over_{eras_length}_significance_statistics.csv'))
print(f'CSV-File exported under the name: agp_over_{eras_length}_significance_statistics.csv')