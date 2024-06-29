import pandas as pd
import statsmodels.api as sm
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.5.4
********************************************************************
REGRESSION RESULTS: MULTIPLE ERAS
********************************************************************
This file allows the computation of regression statistics, regressing
the AGP results on the era, during which the LBP ended. 
This file generates regression summaries for categorical, dummy 
variable regressions based on the dummy variables 'era_long' (15 year
 eras) and 'era_short' (5 year eras).
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


# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data.
df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{ret_w}_vert.csv'), index_col=0)
df['eolbp'] = pd.to_datetime(df['eolbp'])

# Creating a list, which will be changed over the iterations.
categories = eras.copy()

# Iterating over all specified eras.
for i in eras:
    # Adjusting the variable for naming the output file.
    era_constant = f'_{categories[0]}'

    # Changing the eras variable into a categorical variable.
    df[f'{eras_length}'] = pd.Categorical(df[f'{eras_length}'], categories=categories)

    # Deleting values, which do not belong to the eras included in this iteration.
    filtered_df = df[df[f'{eras_length}'].notna()]
    filtered_df.reset_index()

    # Getting the dummy variables
    X = pd.get_dummies(filtered_df[f'{eras_length}'],
                       drop_first=True,
                       dtype=float)

    # Adding a constant
    X = sm.add_constant(X)

    # Define the dependent variable (Y)
    Y = filtered_df['amount_of_months']

    # Fit the regression model
    model = sm.OLS(Y, X).fit()

    # Extract the summary table
    summary_df = pd.DataFrame({
        'coefficients': model.params,
        'standard_errors': model.bse,
        't_values': model.tvalues,
        'p_values': model.pvalues,
        'conf_lower': model.conf_int().iloc[:, 0],
        'conf_upper': model.conf_int().iloc[:, 1]
    })

    # Save the summary to a CSV file
    summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_{eras_length}_dummy_summary{era_constant}.csv'))

    print(f'Regression summary saved to agp_regression_{eras_length}_dummy_summary{era_constant}.csv')

    # Save the summary to a CSV file with the automatic formula.
    with open(os.path.join('07_statistics',f'agp_regression_{eras_length}_dummy_summary_auto{era_constant}.csv'), 'w') as f:
        f.write(model.summary().as_csv())

    print(f'Regression summary saved to agp_regression_{eras_length}_dummy_summary_auto{era_constant}.csv')

    # Adjusting the categorical variable, so that each iteration one category less is considered.
    categories = categories[1:]