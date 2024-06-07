import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
CREATING SUMMARY STATISTICS FOR DIFFERENT ERAS
INCLUDING BELOW 13 MONTHS AGP'S WITH A VALUE OF 0
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


# Specify the different eras
# Always
eras = ['1972-1990', '1991-2005', '2006-2021']
short_eras =[]

# The data frame to store the results is created
# DEFINE WHICH STATISTICAL METRICS YOU WANT INCLUDED AND WRITE THEM INTO THE COLUMN LIST!!!!
column_list = ['identifier','ret_weighting', 'amount_of_factors', 'lbp_length', 'era', 'mean', 'median', 'std', 'var', 'min', '25%', '50%', '75%', 'max', 'skew',
             'kurt', 'count']
summary_stats = pd.DataFrame(columns=column_list, index=[0])

# Filling the new columns with the specific identifier, lbp_length and amount of factors in the portfolios
# Iterating over all different amounts of factors
len_lbp = len(lbp_length_mths_list)
len_fctrs = len(amt_factors_list)
len_eras = len(eras)

for i in range(0,len(returns_weighting_list)):
    df = pd.read_csv(f'agp_{returns_weighting_list[i]}_vert_with_eras.csv', index_col=0)
    for j in range(0, len(amt_factors_list)):
        # Iterating over all different LBP-lengths
        for k in range(0, len(lbp_length_mths_list)):

            # leaving out the first irrelevant date
            for b in range(0, len(eras)):
                    
                # Adding the identifier
                summary_stats.loc[b + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'identifier'] = f'{returns_weighting_list[i]}_{lbp_length_mths_list[k]}_mths_{amt_factors_list[j]}_fctrs_{eras[b]}'
                # Adding the era
                summary_stats.loc[b + k * len_eras + j * len_lbp * len_eras + i * len_lbp * len_fctrs * len_eras, 'era'] = eras[b]
                # Adding the return weighting scheme
                summary_stats.loc[b + k*len_eras + j * len_lbp *len_eras + i * len_lbp * len_fctrs*len_eras, 'ret_weighting'] = returns_weighting_list[i]
                # Adding the length of the LBP
                summary_stats.loc[b + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'lbp_length'] = lbp_length_mths_list[k]
                # Adding the amount of factors
                summary_stats.loc[b + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs*len_eras, 'amount_of_factors'] = amt_factors_list[j]
    
                # CREATE THE STATISTICAL METRICS YOU ADDED INTO THE COLUMN LIST ABOVE!!!!
                # Creating and storing the statistical measures or descriptions in a dataframe 'descr'
                descr = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['era'] == eras[b]), ['amount_of_months']].describe()
                descr.loc['median'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['era'] == eras[b]), ['amount_of_months']].median()
                descr.loc['var'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['era'] == eras[b]), ['amount_of_months']].var()
                descr.loc['skew'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['era'] == eras[b]), ['amount_of_months']].skew()
                descr.loc['kurt'] = df.loc[(df['amount_of_factors'] == amt_factors_list[j]) & (df['lbp_length'] == lbp_length_mths_list[k]) & (df['era'] == eras[b]), ['amount_of_months']].kurt()
    
                #print(descr)
    
                for x in column_list[5:]:
                    summary_stats.loc[b + k*len_eras + j * len_lbp *len_eras + i * len_lbp*len_fctrs *len_eras, x] = descr.loc[x, 'amount_of_months']


summary_stats.to_csv('agp_over_eras_summary_statistics_incl.csv')
print(f'CSV-File exported under the name: agp_over_eras_summary_statistics_incl.csv')
