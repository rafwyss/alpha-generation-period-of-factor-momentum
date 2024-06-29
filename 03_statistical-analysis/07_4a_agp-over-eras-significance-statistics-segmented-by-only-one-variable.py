import pandas as pd
import scipy.stats as stats
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.4a
********************************************************************
SIGNIFICANCE STATISTICS OVER MULTIPLE ERAS SEGMENTED BY ONE ONLY 
INPUT VARIABLE: LBP-LENGTH OR PERCENTILE
********************************************************************
This file allows the computation of significance statistics for two 
different era lengths: 15 years or 5 years, segmented by only one 
input variable. This means that e.g. the results for one percentile
are aggregated over all LBP-lengths and vice versa. Significance 
statistics are still generated for all return weighting methods 
together in one single file.
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

variable = ['percentiles', 'lbp_lengths']
for a in variable:
    # SEGMENTED BY PERCENTILES
    if a == 'percentiles':
        # The data frame to store the results is created
        # DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
        column_list = ['identifier', 'era', 'ret_weighting', 'amount_of_factors', 'mean', 'std', 'CI_bottom', 'CI_top',
                       't_stat', 'p_value']
        significance_stats = pd.DataFrame(columns=column_list, index=[0])

        # Iterating over all return weighting methods
        for i in range(0, len(returns_weighting_list)):
            # Importing the corresponding AGP results data
            df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{returns_weighting_list[i]}_vert.csv'), index_col=0)
            # Iterating over all percentiles
            for j in range(0, len(amt_factors_list)):
                # Iterating over all different LBP-lengths
                # leaving out the first irrelevant date
                for b in range(0, len(eras)):

                    # Adding the identifier
                    significance_stats.loc[
                        b + j * len_eras + i * len_fctrs * len_eras, 'identifier'] = f'{returns_weighting_list[i]}_{amt_factors_list[j]}_fctrs_{eras[b]}'
                    # Adding the era
                    significance_stats.loc[b + j * len_eras + i * len_fctrs * len_eras, 'era'] = eras[b]
                    # Adding the return weighting scheme
                    significance_stats.loc[b + j * len_eras + i * len_fctrs * len_eras, 'ret_weighting'] = \
                    returns_weighting_list[i]
                    # Adding the amount of factors
                    significance_stats.loc[b + j * len_eras + i * len_fctrs * len_eras, 'amount_of_factors'] = \
                    amt_factors_list[j]

                    total_count = ((df['amount_of_factors'] == amt_factors_list[j]) & (df[f'{eras_length}'] == eras[b])).sum()

                    # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
                    describe = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df[f'{eras_length}'] == eras[b]), [
                        'amount_of_months']].describe()
                    descr = describe.loc[['mean', 'std']]

                    # CONFIDENCE INTERVAL
                    ci_interval = stats.t.interval(confidence=0.05,
                                                   df=total_count - 1,
                                                   loc=descr.loc['mean', 'amount_of_months'],
                                                   scale=descr.loc['std', 'amount_of_months'])

                    descr.loc['CI_bottom'] = ci_interval[0]
                    descr.loc['CI_top'] = ci_interval[1]

                    # HYPOTHESIS TESTING
                    t_test = stats.ttest_1samp(a=df.loc[
                        (df['amount_of_factors'] == amt_factors_list[j]) & (df[f'{eras_length}'] == eras[b]), ['amount_of_months']],
                                               popmean=24, alternative='greater')

                    descr.loc['t_stat'] = t_test[0][0]
                    descr.loc['p_value'] = t_test[1][0]

                    for x in column_list[4:]:
                        significance_stats.loc[b + j * len_eras + i * len_fctrs * len_eras, x] = descr.loc[
                            x, 'amount_of_months']
        # Exporting the results as a CSV file.
        significance_stats.to_csv(os.path.join('07_statistics',f'agp_over_{eras_length}_significance_statistics_segmented_by_{a}.csv'))
        print(f'CSV-File exported under the name: agp_over_{eras_length}_summary_statistics_segmented_by_{a}.csv')

    # SEGMENTED BY LBP-LENGTH
    elif a == 'lbp_lengths':
        # The data frame to store the results is created
        # DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
        column_list = ['identifier', 'era','ret_weighting', 'lbp_length', 'mean', 'std', 'CI_bottom', 'CI_top', 't_stat', 'p_value']
        significance_stats = pd.DataFrame(columns=column_list, index=[0])

        # Iterating over all return weighting methods
        for i in range(0, len(returns_weighting_list)):
            # Importing the corresponding AGP results data
            df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{returns_weighting_list[i]}_vert.csv'), index_col=0)
            # Iterating over all different LBP-lengths
            for k in range(0, len(lbp_length_mths_list)):

                # leaving out the first irrelevant date
                for b in range(0, len(eras)):

                    # Adding the identifier
                    significance_stats.loc[
                        b + k * len_eras + i * len_lbp * len_eras, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{eras[b]}'
                    # Adding the era
                    significance_stats.loc[
                        b + k * len_eras + i * len_lbp * len_eras, 'era'] = eras[b]
                    # Adding the return weighting scheme
                    significance_stats.loc[
                        b + k * len_eras + i * len_lbp * len_eras, 'ret_weighting'] = \
                    returns_weighting_list[i]
                    # Adding the length of the LBP
                    significance_stats.loc[
                        b + k * len_eras + i * len_lbp * len_eras, 'lbp_length'] = \
                    lbp_length_mths_list[k]



                    total_count = ((
                            df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{eras_length}'] == eras[b])).sum()

                    # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
                    describe = df.loc[
                        ((df['lbp_length'] == lbp_length_mths_list[k]) & (
                                    df[f'{eras_length}'] == eras[b])), ['amount_of_months']].describe()
                    descr = describe.loc[['mean', 'std']]

                    # CONFIDENCE INTERVAL
                    ci_interval = stats.t.interval(confidence=0.05,
                                                   df=total_count - 1,
                                                   loc=descr.loc['mean', 'amount_of_months'],
                                                   scale=descr.loc['std', 'amount_of_months'])

                    descr.loc['CI_bottom'] = ci_interval[0]
                    descr.loc['CI_top'] = ci_interval[1]

                    # HYPOTHESIS TESTING
                    t_test = stats.ttest_1samp(a=df.loc[
                        (df['lbp_length'] == lbp_length_mths_list[k]) & (
                                    df[f'{eras_length}'] == eras[b]), ['amount_of_months']], popmean=24, alternative='greater')

                    descr.loc['t_stat'] = t_test[0][0]
                    descr.loc['p_value'] = t_test[1][0]

                    for x in column_list[4:]:
                        significance_stats.loc[b + k * len_eras + i * len_lbp * len_eras, x] = descr.loc[x, 'amount_of_months']

        # Exporting the results as a CSV file.
        significance_stats.to_csv(os.path.join('07_statistics',f'agp_over_{eras_length}_significance_statistics_segmented_by_{a}.csv'))
        print(f'CSV-File exported under the name: agp_over_{eras_length}_summary_statistics_segmented_by_{a}.csv')