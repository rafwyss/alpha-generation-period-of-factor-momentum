import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

percentiles_start = "_33%"

df = pd.read_csv('agp_vw_cap_vert.csv', index_col=0)

df['eolbp'] = pd.to_datetime(df['eolbp'])
df['amount_of_factors'] = df['amount_of_factors'].astype(str)
df.loc[df['amount_of_factors']=='51', ['amount_of_factors']] = 'Top Tercile'
df.loc[df['amount_of_factors']=='30', ['amount_of_factors']] = 'Top Quintile'
df.loc[df['amount_of_factors']=='15', ['amount_of_factors']] = 'Top Decile'
df.loc[df['amount_of_factors']=='7', ['amount_of_factors']] = 'Top 5%'

print(df)

categories = [#'Top 5%',
              #'Top Decile',
              #'Top Quintile',
              'Top Tercile',
              ]

df['amount_of_factors'] = pd.Categorical(df['amount_of_factors'], categories=categories)
print(df)

filtered_df = df[df['amount_of_factors'].notna()]
filtered_df.reset_index()
print(filtered_df)


# Convert 'ret_w' to dummy variables and drop 'vw'
X = pd.get_dummies(filtered_df['amount_of_factors'], drop_first=True, dtype=float)

# Add a constant
X = sm.add_constant(X)

# Define the dependent variable (Y)
Y = filtered_df['amount_of_months']

# Fit the regression model
model = sm.OLS(Y, X).fit()

print(model.summary())

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
summary_df.to_csv(f'agp_regression_percentiles_dummy_summary{percentiles_start}.csv')

print(f'Regression summary saved to agp_regression_percentiles_dummy_summary{percentiles_start}.csv')

# Save the summary to a CSV file
with open(f'agp_regression_lbp_length_percentiles_summary_auto{percentiles_start}.csv', 'w') as f:
    f.write(model.summary().as_csv())
print(f'Regression summary saved to agp_regression_percentiles_dummy_summary_auto{percentiles_start}.csv')

