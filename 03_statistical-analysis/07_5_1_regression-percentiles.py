import pandas as pd
import statsmodels.api as sm
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Statistical analysis Python-Script Nr. 7.5.1
********************************************************************
REGRESSION RESULTS: PERCENTILES
********************************************************************
This file allows the computation of regression statistics, regressing
the AGP results on the percentiles (amount of factors) used to 
compute the AGP results. 
By default this file generates regression summaries for categorical 
dummy variable regressions based on the dummy variables 'Percentile'.
However, this file can also generate regression statistics for 
liner (non-categorical) regressions, without converting the 
percentiles to dummy variables, meaning the regression is based on 
the amount of factors per portfolio.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""


# Specify the regression type!
# Options: For categorical, dummy variable regression: 'categorical-dummy'. For normal linear regression: 'linear'.
regression_type = 'categorical-dummy'

# Specify the percentile (amount of factors)
amt_factors = [51, 30, 15, 7]

# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data.
df = pd.read_csv(os.path.join('..', '02_AGP-calculation', f'agp_{ret_w}_vert.csv'), index_col=0)
df['eolbp'] = pd.to_datetime(df['eolbp'])

# Creating a list, which will be changed over the iterations.
categories = amt_factors.copy()

# CATEGORICAL, DUMMY REGRESSION
if regression_type == 'categorical-dummy':
    # Iterating over all percentiles
    for i in amt_factors:
        # Adjusting the variable for naming the output file.
        percentile_constant = f'_{categories[0]}'

        # Changing the percentiles into a categorical variable.
        df['amount_of_factors'] = pd.Categorical(df['amount_of_factors'], categories=categories)

        # Deleting values, which do not belong to the percentiles included in this iteration.
        filtered_df = df[df['amount_of_factors'].notna()]
        filtered_df.reset_index()

        # Getting the dummy variables
        X = pd.get_dummies(filtered_df['amount_of_factors'],
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
        summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_percentiles_dummy_summary{percentile_constant}.csv'))

        print(f'Regression summary saved to agp_regression_percentiles_dummy_summary{percentile_constant}.csv')

        # Save the summary to a CSV file with the automatic formula.
        with open(os.path.join('07_statistics',f'agp_regression_percentiles_dummy_summary_auto{percentile_constant}.csv'), 'w') as f:
            f.write(model.summary().as_csv())

        print(f'Regression summary saved to agp_regression_percentiles_dummy_summary_auto{percentile_constant}.csv')

        # Adjusting the categorical variable, so that each iteration one category less is considered.
        categories = categories[1:]

# LINEAR REGRESSION
elif regression_type == 'linear':

    # Define the independent variable
    X = df['amount_of_factors']

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
    summary_df.to_csv(os.path.join('07_statistics',f'agp_regression_percentiles_linear_summary.csv'))

    print(f'Regression summary saved to agp_regression_percentiles_linear_summary.csv')

    # Save the summary to a CSV file with the automatic formula.
    with open(os.path.join('07_statistics',f'agp_regression_percentiles_linear_summary_auto.csv'), 'w') as f:
        f.write(model.summary().as_csv())

    print(f'Regression summary saved to agp_regression_percentiles_linear_summary_auto.csv')