import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Data visualization Python-Script Nr. 8.3
********************************************************************
SCATTER PLOT VISUALIZING ALL AGP RESULTS
********************************************************************
This file allows the generation of a scatter plot of AGP results 
over the entire time frame from 1971-2021. 
The file also allows for further segmentation by percentiles or 
LBP-lengths.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the segmentation.
# Options: For no further segmentation: 'none'. For further segmentation by percentiles: 'percentiles'. For further segmentation by LBP-length: 'lbp_length'
segmentation = 'lbp_length'

# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data
df = pd.read_csv(os.path.join('..', '02_AGP-calculation',f'agp_{ret_w}_vert.csv'))
df['eolbp'] = pd.to_datetime(df['eolbp'])


if segmentation == 'none':
    # Creating a scatter Plot
    sns.set(style='darkgrid')
    plt.rcParams.update({'axes.facecolor': '#f5f5f5', })

    plt.figure(figsize=(10, 6))

    sns.scatterplot(data=df, x='eolbp', y='amount_of_months',
                    edgecolors=None,
                    )

    plt.title('Alpha-generation periods (1972 - 2021)', fontsize=16, fontweight='bold', pad=16)
    plt.xlabel(('End of LBP [$T_{L}$]'), fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    plt.savefig(os.path.join('08_visualizations',f'agp_scatterplot_{ret_w}.png'), dpi=800, bbox_inches='tight')

elif segmentation == 'percentiles':
    # Creating a scatter Plot
    sns.set(style='darkgrid')
    plt.rcParams.update({'axes.facecolor': '#f5f5f5', })

    plt.figure(figsize=(10, 6))

    sns.scatterplot(data=df, x='eolbp', y='amount_of_months',
                    hue='amount_of_factors',
                    legend='full',
                    edgecolors=None,
                    )

    labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']  # Custom labels
    plt.legend( labels, title='Percentile')

    plt.title('Alpha-generation periods (1972 - 2021)', fontsize=16, fontweight='bold', pad=16)
    plt.xlabel(('End of LBP [$T_{L}$]'), fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    plt.savefig(os.path.join('08_visualizations',f'agp_scatterplot_{ret_w}_by_percentiles.png'), dpi=800, bbox_inches='tight')

elif segmentation == 'lbp_length':
    # Creating a scatter Plot
    sns.set(style='darkgrid')
    plt.rcParams.update({'axes.facecolor': '#f5f5f5', })

    plt.figure(figsize=(10, 6))

    sns.scatterplot(data=df, x='eolbp', y='amount_of_months',
                    hue='lbp_length',
                    legend='full',
                    edgecolors=None,
                    )

    plt.legend(title='LBP-length [in months]')

    plt.title('Alpha-generation periods (1972 - 2021)', fontsize=16, fontweight='bold', pad=16)
    plt.xlabel(('End of LBP [$T_{L}$]'), fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    plt.savefig(os.path.join('08_visualizations',f'agp_scatterplot_{ret_w}_by_lbp_length.png'), dpi=800, bbox_inches='tight')