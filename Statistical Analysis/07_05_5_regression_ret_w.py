import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

ret_w_start =''

# Read the data
df = pd.read_csv('agp_combined_vert.csv')

# Convert 'eolbp' to datetime
df['eolbp'] = pd.to_datetime(df['eolbp'])

# Ensure 'amount_of_months' is numeric
df['amount_of_months'] = pd.to_numeric(df['amount_of_months'], errors='coerce')

categories=['vw','vw_cap','ew']

# Manually specify the categories and order for 'ret_w'
df['ret_w'] = pd.Categorical(df['ret_w'], categories=categories)

filtered_df = df[df['ret_w'].notna()]

# Convert 'ret_w' to dummy variables and drop 'vw'
X = pd.get_dummies(filtered_df['ret_w'], drop_first=True, dtype=float)

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
summary_df.to_csv(f'agp_regression_ret_w_summary{ret_w_start}.csv')

print(f'Regression summary saved to agp_regression_ret_w_summary{ret_w_start}.csv')

# Save the summary to a CSV file
with open(f'agp_regression_ret_w_summary_auto{ret_w_start}.csv', 'w') as f:
    f.write(model.summary().as_csv())
print(f'Regression summary saved to agp_regression_ret_w_summary_auto{ret_w_start}.csv')

"""
# Extract the parameters for the regression line
intercept, slope = model.params

sns.set(style='darkgrid')
plt.rcParams.update({'axes.facecolor': '#f5f5f5',
                     #'legend.loc': 'upper right'
                     })

plt.figure(figsize=(10,6))



# Create the scatter plot
sns.scatterplot(df, x = 'ret_w', y = 'amount_of_months',
                #hue='amount_of_factors',
                color='#ad7a94',
                #edgecolor=None
                )

# Create the regression line
regression_line = intercept + slope * df['ret_w']
plt.plot(df['ret_w'], regression_line, color='black', label='Regression Line')

# Add labels and title
plt.xlabel('Return weighting method', fontsize = 14, fontweight='semibold', )
plt.ylabel('Alpha-generation period [in months]', fontsize = 14, fontweight='semibold',)
#plt.title('Scatter Plot with OLS Regression Line')
plt.legend()


labels = ['Equally weighted', 'Capped value weighted','Value weighted']
plt.xticks(ticks=['ew','vw_cap','vw'], labels=labels)


plt.show()
#plt.savefig('agp_regression_ret_w.png', dpi=800, bbox_inches='tight')
print("Figure saved under name: 'agp_regression_ret_w.png'")

"""