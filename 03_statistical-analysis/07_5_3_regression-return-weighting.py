import pandas as pd
import statsmodels.api as sm
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.5.3
********************************************************************
REGRESSION RESULTS: RETURN WEIGHTING METHOD
********************************************************************
This file allows the computation of regression statistics, regressing
the AGP results on the return weighting method used to compute the 
underlying factor returns. 
This file generates regression summaries for categorical dummy 
variable regressions based on the dummy variables 'return weighting 
method'.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Configure the return weighting methods.
# Possible options: 'ew' = equally weighted, 'vw' = value weighted, 'vw_cap' for value weighted capped at the NYSE 80th percentile
returns_weighting = [#'ew', 'vw',
                          'vw_cap'
                          ]

# Importing the relevant data
df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_combined_vert.csv'), index_col=0)
df['eolbp'] = pd.to_datetime(df['eolbp'])

# Creating a list, which will be changed over the iterations.
categories = returns_weighting.copy()

# Iterating over all return weighting methods
for i in returns_weighting:
    # Adjusting the variable for naming the output file.
    return_weighting_constant = f'_{categories[0]}'

    # Changing the return weighting methods into a categorical variable.
    df['ret_w'] = pd.Categorical(df['ret_w'], categories=categories)

    # Deleting values, which do not belong to the return weighting methods used in this iteration.
    filtered_df = df[df['ret_w'].notna()]
    filtered_df.reset_index()

    # Getting the dummy variables
    X = pd.get_dummies(filtered_df['ret_w'],
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
    summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_return_weighting_dummy_summary{return_weighting_constant}.csv'))

    print(f'Regression summary saved to agp_regression_return_weighting_dummy_summary{return_weighting_constant}.csv')

    # Save the summary to a CSV file with the automatic formula.
    with open(os.path.join('07_statistics',f'agp_regression_return_weighting_dummy_summary_auto{return_weighting_constant}.csv'), 'w') as f:
        f.write(model.summary().as_csv())

    print(f'Regression summary saved to agp_regression_return_weighting_dummy_summary_auto{return_weighting_constant}.csv')

    # Adjusting the categories, so that each iteration one category less is considered.
    categories = categories[1:]