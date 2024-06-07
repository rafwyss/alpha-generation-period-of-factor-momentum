import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

lbp_length_start = "_12"

df = pd.read_csv('agp_vw_cap_vert.csv', index_col=0)

df['eolbp'] = pd.to_datetime(df['eolbp'])

"""categories = [12,
            24,
            36,
            48,
            60,
            72,
            84,
            96,
            108,
            120]"""

#df['lbp_length'] = pd.Categorical(df['lbp_length'], categories=categories)
print(df)

filtered_df = df[df['lbp_length'].notna()]
filtered_df.reset_index()
print(filtered_df)


# Convert 'ret_w' to dummy variables and drop 'vw'
X = pd.get_dummies(filtered_df['lbp_length'],
                    drop_first=True,
                   dtype=float)

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
summary_df.to_csv(f'agp_regression_lbp_length_dummy_summary{lbp_length_start}.csv')

print(f'Regression summary saved to agp_regression_lbp_length_dummy_summary{lbp_length_start}.csv')

# Save the summary to a CSV file
with open(f'agp_regression_lbp_length_dummy_summary_auto{lbp_length_start}.csv', 'w') as f:
    f.write(model.summary().as_csv())
print(f'Regression summary saved to agp_regression_lbp_length_dummy_summary_auto{lbp_length_start}.csv')
