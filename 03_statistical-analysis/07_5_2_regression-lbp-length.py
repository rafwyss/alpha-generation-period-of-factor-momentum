import pandas as pd
import statsmodels.api as sm
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.5.2
********************************************************************
REGRESSION RESULTS: LBP-LENGTH
********************************************************************
This file allows the computation of regression statistics, regressing
the AGP results on the LBP-length used to compute the AGP results. 
By default this file generates regression summaries for categorical 
dummy variable regressions based on the dummy variables 'LBP-length'.
However, this file can also generate regression statistics for 
liner (non-categorical) regressions, without converting the 
LBP-lengths to dummy variables.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the regression type!
# Options: For categorical, dummy variable regression: 'categorical-dummy'. For normal linear regression: 'linear'.
regression_type = 'linear'

# Specify the different LBP-lengths!
lbp_length = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]

# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data.
df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{ret_w}_vert.csv'), index_col=0)
df['eolbp'] = pd.to_datetime(df['eolbp'])

# Creating a list, which will be changed over the iterations.
categories = lbp_length.copy()

# CATEGORICAL, DUMMY REGRESSION
if regression_type == 'categorical-dummy':
    # Iterating over all LBP-lengths
    for i in lbp_length:
        # Adjusting the variable for naming the output file.
        lbp_length_start = f'_{categories[0]}'

        # Changing the LBP-length into a categorical variable.
        df['lbp_length'] = pd.Categorical(df['lbp_length'], categories=categories)

        # Deleting values, which do not belong to the LBP-categories.
        filtered_df = df[df['lbp_length'].notna()]
        filtered_df.reset_index()

        # Getting the dummy variables
        X = pd.get_dummies(filtered_df['lbp_length'],
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
        summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_lbp_length_dummy_summary{lbp_length_start}.csv'))

        print(f'Regression summary saved to agp_regression_lbp_length_dummy_summary{lbp_length_start}.csv')

        # Save the summary to a CSV file with the automatic formula.
        with open(os.path.join('07_statistics',f'agp_regression_lbp_length_dummy_summary_auto{lbp_length_start}.csv'), 'w') as f:
            f.write(model.summary().as_csv())

        print(f'Regression summary saved to agp_regression_lbp_length_dummy_summary_auto{lbp_length_start}.csv')

        # Adjusting the categories, so that each iteration one category less is considered.
        categories = categories[1:]

# LINEAR REGRESSION
elif regression_type == 'linear':

    # Define the independent variable
    X = df['lbp_length']

    # Define the dependent variable (Y)
    Y = df['amount_of_months']

    # Adding a constant
    X = sm.add_constant(X)

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
    summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_lbp_length_linear_summary.csv'))

    print(f'Regression summary saved to agp_regression_lbp_length_linear_summary.csv')

    # Save the summary to a CSV file with the automatic formula.
    with open(os.path.join('07_statistics',f'agp_regression_lbp_length_linear_summary_auto.csv'), 'w') as f:
        f.write(model.summary().as_csv())

    print(f'Regression summary saved to agp_regression_lbp_length_linear_summary_auto.csv')