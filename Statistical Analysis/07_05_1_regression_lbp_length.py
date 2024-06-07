import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('agp_combined_vert.csv')


df = data.loc[data['ret_w'] == 'vw_cap'].copy()

df['eolbp'] = pd.to_datetime(df['eolbp'])

X = df['lbp_length']

Y = df['amount_of_months']

X = sm.add_constant(X)

model = sm.OLS(Y,X).fit()

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
summary_df.to_csv('agp_regression_lbp_length_summary.csv')

print("Regression summary saved to 'agp_regression_lbp_length_summary.csv'.")

# Save the summary to a CSV file
with open('agp_regression_lbp_length_summary_auto.csv', 'w') as f:
    f.write(model.summary().as_csv())
print("Regression summary saved to 'agp_regression_lbp_length_summary_auto.csv'.")


# Extract the parameters for the regression line
intercept, slope = model.params

sns.set(style='darkgrid')
plt.rcParams.update({'axes.facecolor': '#f5f5f5',
                     #'legend.loc': 'upper right'
                     })

plt.figure(figsize=(10,6))



# Create the scatter plot
sns.scatterplot(df, x = 'lbp_length', y = 'amount_of_months',
                #hue='amount_of_factors',
                color='#ad7a94',
                #edgecolor=None
                )

# Create the regression line
regression_line = intercept + slope * df['lbp_length']
plt.plot(df['lbp_length'], regression_line, color='black', label='Regression Line')

# Add labels and title
plt.xlabel('LBP-length [in months]', fontsize = 14, fontweight='semibold', )
plt.ylabel('Alpha-generation period [in months]', fontsize = 14, fontweight='semibold',)
#plt.title('Scatter Plot with OLS Regression Line')
plt.legend()



new_labels = df['lbp_length'].unique()
#print(new_labels)
plt.xticks(ticks=new_labels)

#plt.show()
plt.savefig('agp_regression_lbp_length.png', dpi=800, bbox_inches='tight')
print("Figure saved under name: 'agp_regression_lbp_length.png'")