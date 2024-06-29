import pandas as pd
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.3
********************************************************************
SUMMARY STATISTICS FOR ALL DIFFERENT VARIABLE COMBINATIONS OVER 
MULTIPLE ERAS
********************************************************************
This file allows the computation of summary statistics for two 
different era lengths: 15 years or 5 years. 
Summary statistics are generated for all return weighting 
methods together in one single file.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED 
WEIGHTING METHOD, AND INCLUDING THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the length of the era you want!
# Options: For 3 eras à 15 years: 'eras_long'. For 8 eras à 5 years: 'eras_short'.
era_length = 'eras_long'

eras = []
if era_length == 'eras_long':
    eras = ['1972-1990', '1991-2005', '2006-2021']
elif era_length == 'eras_short':
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
lbp_length_mths_list = [12,
                        24, 36, 48, 60, 72, 84, 96, 108, 120
                        ]

# The data frame to store the results is created
# Statistical measures are defined.
column_list = ['identifier','ret_weighting', 'amount_of_factors', 'lbp_length', 'era', 'mean', 'median', 'std', 'var', 'min', '25%', '50%', '75%', 'max', 'skew',
             'kurt', 'count']
summary_stats = pd.DataFrame(columns=column_list, index=[0])


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
                # Filling the new columns with the specific identifier, era, lbp_length and amount of factors in the portfolios
                # Adding the identifier
                summary_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{amt_factors_list[j]}_fctrs_{eras[e]}'
                # Adding the era
                summary_stats.loc[e + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'era'] = eras[e]
                # Adding the return weighting scheme
                summary_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp * len_fctrs*len_eras, 'ret_weighting'] = returns_weighting_list[i]
                # Adding the length of the LBP
                summary_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'lbp_length'] = lbp_length_mths_list[k]
                # Adding the amount of factors
                summary_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'amount_of_factors'] = amt_factors_list[j]
    
                # CREATE THE STATISTICAL METRICS YOU ADDED INTO THE COLUMN LIST ABOVE!!!!
                # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
                descr = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{era_length}'] == eras[e]), ['amount_of_months']].describe()
                descr.loc['median'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{era_length}'] == eras[e]), ['amount_of_months']].median()
                descr.loc['var'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{era_length}'] == eras[e]), ['amount_of_months']].var()
                descr.loc['skew'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{era_length}'] == eras[e]), ['amount_of_months']].skew()
                descr.loc['kurt'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df[f'{era_length}'] == eras[e]), ['amount_of_months']].kurt()

                # Adding the statistical measures into the results data frame.
                for x in column_list[5:]:
                    summary_stats.loc[e + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs *len_eras, x] = descr.loc[x, 'amount_of_months']

# Exporting the results as a CSV file.
summary_stats.to_csv(os.path.join('07_statistics',f'agp_over_{era_length}_summary_statistics.csv'))
print(f'CSV-File exported under the name: agp_over_{era_length}_summary_statistics.csv')
