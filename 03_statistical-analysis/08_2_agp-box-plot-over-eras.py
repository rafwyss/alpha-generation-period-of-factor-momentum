import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Data visualization Python-Script Nr. 8.2
********************************************************************
BOX PLOT FOR AGP RESULTS SEGMENTED BY MULTIPLE SHORT OR LONG ERAS
********************************************************************
This file allows the generation of box plots of AGP results, 
segmented by multiple eras. Choose either 'eras_long' for 3 eras à
15 years each and 'eras_short' à 5 years each.
The file also allows for further segmentation by percentiles or 
LBP-lengths.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the length of the era you want!
# Options: For 3 eras à 15 years: 'eras_long'. For 8 eras à 5 years: 'eras_short'.
eras_length = 'eras_short'

# Specify the segmentation.
# Options: For no further segmentation: 'none'. For further segmentation by percentiles: 'percentiles'. For further segmentation by LBP-length: 'lbp_length'
segmentation = 'none'

# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data
df = pd.read_csv(os.path.join('..', '02_AGP-calculation',f'agp_{ret_w}_vert.csv'))

# Customizing the background color
sns.set(style='darkgrid')
plt.rcParams.update({'axes.facecolor': '#f5f5f5',})

# SEGMENTING BY LONG 15 YEAR ERAS
if eras_length == 'eras_long':
    # NO FURTHER SEGMENTATION
    if segmentation == 'none':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_long', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              )

        # Setting specific colors
        colors = ['#e8d4d0', '#d6aeb4', '#9d6b8a']

        for i, patch in enumerate(boxplot.patches):
            face_color = colors[i % len(colors)]
            patch.set_facecolor(face_color)


        # Creating the values for descriptions
        medians = df.groupby([f'{eras_length}'])['amount_of_months'].median().values
        means = df.groupby([f'{eras_length}'])['amount_of_months'].mean().values
        max_vals = df.groupby([f'{eras_length}'])['amount_of_months'].max().values

        # Adding the descriptions
        for i, group in enumerate(df[f'{eras_length}'].unique()):
            median = medians[i]
            mean = means[i]
            max_val = max_vals[i]

            if i == 2:
                j = -4
                place = 'top'
            else:
                j = 1
                place = 'bottom'

            # Median
            plt.text(i, median + j, f'{median}', horizontalalignment='center', va=place,
                     color='black', weight='semibold', fontsize=11)

            # Maximum
            plt.text(i, max_val, f'{max_val}', horizontalalignment='center', va='bottom',
                     color='black', weight='light', fontsize=11)


        plt.xlabel('Different eras [ ≈15 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}.png'), dpi=800, bbox_inches='tight')


    # FURTHER SEGMENTATION BY PERCENTILES
    elif segmentation == 'percentiles':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_long', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              hue='amount_of_factors',
                              legend='full'
                              )

        handles, labels = boxplot.get_legend_handles_labels()
        labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']  # Custom labels
        plt.legend(handles, labels, title='Percentile')

        plt.xlabel('Different eras [ ≈15 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}_by_percentiles.png'), dpi=800, bbox_inches='tight')

    # FURTHER SEGMENTATION BY LBP-LENGTH
    elif segmentation == 'lbp_length':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_long', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              hue='lbp_length',
                              legend='full'
                              )

        plt.legend(title='LBP-length')

        plt.xlabel('Different eras [ ≈15 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}_by_lbp_length.png'), dpi=800, bbox_inches='tight')


# SEGMENTING BY SHORT 5 YEAR ERAS
elif eras_length == 'eras_short':
    # NO FURTHER SEGMENTATION
    if segmentation == 'none':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_short', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              )

        # Setting specific colors
        colors = ['#e8d4d0', '#debdbd', '#d0a7af', '#c08f9f', '#ad7a94', '#956586', '#7c5378', '#614166', '#473252', '#2d223a']

        for i, patch in enumerate(boxplot.patches):
            face_color = colors[i % len(colors)]
            patch.set_facecolor(face_color)

        medians = df.groupby([f'{eras_length}'])['amount_of_months'].median().values
        means = df.groupby([f'{eras_length}'])['amount_of_months'].mean().values
        max_vals = df.groupby([f'{eras_length}'])['amount_of_months'].max().values

        # Adding the descriptions
        for i, group in enumerate(df[f'{eras_length}'].unique()):
            median = medians[i]
            mean = means[i]
            max_val = max_vals[i]

            if i == 4 or i == 7:
                j = -4
                place = 'top'
            elif i == 5:
                j = -2
                place = 'top'
            else:
                j = 1
                place = 'bottom'

            # Median
            plt.text(i, median + j, f'{median}', horizontalalignment='center', va=place,
                     color='black', weight='semibold', fontsize=11)

            # Maximum
            plt.text(i, max_val, f'{max_val}', horizontalalignment='center', va='bottom',
                     color='black', weight='light', fontsize=11)


        plt.xlabel('Different eras [ ≈5 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}.png'), dpi=800, bbox_inches='tight')

    # FURTHER SEGMENTATION BY PERCENTILES
    elif segmentation == 'percentiles':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_short', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              hue='amount_of_factors',
                              legend='full'
                              )

        handles, labels = boxplot.get_legend_handles_labels()
        labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']  # Custom labels
        plt.legend(handles, labels, title='Percentile')

        plt.xlabel('Different eras [ ≈5 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}_by_percentiles.png'), dpi=800, bbox_inches='tight')

    # FURTHER SEGMENTATION BY LBP-LENGTH
    elif segmentation == 'lbp_length':
        plt.figure(figsize=(10, 6))

        # Generating the box plot
        boxplot = sns.boxplot(data=df, x='eras_short', y='amount_of_months',
                              whis=(0, 100),
                              fill=True,
                              medianprops={'color': 'black', 'linewidth': 1},
                              linecolor='black',
                              linewidth=1,
                              hue='lbp_length',
                              legend='full'
                              )

        plt.legend(title='LBP-length')

        plt.xlabel('Different eras [ ≈5 years]', fontsize=14, fontweight='semibold', )
        plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

        plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_over_{eras_length}_{ret_w}_by_lbp_length.png'), dpi=800, bbox_inches='tight')