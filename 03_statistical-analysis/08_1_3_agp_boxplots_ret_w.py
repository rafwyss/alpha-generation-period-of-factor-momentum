import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Data visualization Python-Script Nr. 8.1.3
********************************************************************
BOX PLOT FOR AGP RESULTS 1971-2021 SEGMENTED BY UNDERLYING RETURN 
WEIGHTING METHODS
********************************************************************
This file allows the generation of box plots of AGP results over 
the entire period from 1971 to 2021, segmented by the underlying 
return weighting methods.
The file also allows for further segmentation by percentiles or 
LBP-lengths.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_combined_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the segmentation.
# Options: For no further segmentation: 'none'. For further segmentation by percentiles: 'percentiles'. For further segmentation by LBP-length: 'lbp_length'
segmentation = 'none'


# Importing the relevant data
df = pd.read_csv(os.path.join('..', '02_AGP-calculation',f'agp_combined_vert.csv'))


# Customizing the background color
sns.set(style='darkgrid')
plt.rcParams.update({'axes.facecolor': '#f5f5f5',
                     'legend.loc': 'upper right'}
                    )

# NO FURTHER SEGMENTATION
if segmentation == 'none':
    # Starting the figure
    plt.figure(figsize=(10,6))

    # Generating the box plot
    boxplot = sns.boxplot(data=df, x='ret_w', y='amount_of_months',
                          whis=(0, 100),
                          fill=True,
                          medianprops={'color': 'black', 'linewidth': 1.5},
                          linecolor='#2d223a',
                          linewidth=1,
                          legend='full'
                          )

    # Setting specific colors
    colors = ['#e8d4d0', '#d6aeb4', '#9d6b8a']

    for i, patch in enumerate(boxplot.patches):
        face_color = colors[i % len(colors)]
        patch.set_facecolor(face_color)

    plt.xlabel('Return weighting methods', fontsize = 14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize = 14, fontweight='semibold',)

    new_labels = ['Equally weighted', 'Capped value weighted', 'Value weighted']
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels)

    medians = df.groupby(['ret_w'])['amount_of_months'].median().values
    medians[1], medians[2] = medians[2], medians[1]
    means = df.groupby(['ret_w'])['amount_of_months'].mean().values
    means[1], means[2] = means[2], means[1]
    max_vals = df.groupby(['ret_w'])['amount_of_months'].max().values
    max_vals[1], max_vals[2] = max_vals[2], max_vals[1]

    # Adding descriptions to the plot
    for i, group in enumerate(df['ret_w'].unique()):

        median = medians[i]
        mean = means[i]
        max_val = max_vals[i]

        # Adjusting the positioning
        if i == 2:
            j = -2
            place = 'top'
        else:
            j = 0
            place = 'bottom'

        # Adding the median value description
        plt.text(i, median + j, f'{median}', horizontalalignment='center', va=place,
                 color='black', weight='semibold', fontsize=11)

        # Adding the maximum value description
        plt.text(i, max_val, f'{max_val}', horizontalalignment='center', va='bottom',
                 color='black', weight='light', fontsize=11)

    plt.savefig(os.path.join('08_visualizations','agp_boxplot_return_weighting.png'), dpi=800, bbox_inches='tight')


# FURTHER SEGMENTATION BY PERCENTILES
elif segmentation == 'percentiles':
    # Starting the figure
    plt.figure(figsize=(10, 6))

    # Generating the box plot
    boxplot = sns.boxplot(data=df, x='ret_w', y='amount_of_months',
                          whis=(0, 100),
                          fill=True,
                          medianprops={'color': 'black', 'linewidth': 1.5},
                          linecolor='#2d223a',
                          linewidth=1,
                          hue='amount_of_factors',
                          legend='full'
                          )

    handles, labels = boxplot.get_legend_handles_labels()
    labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']  # Custom labels
    plt.legend(handles, labels, title='Percentile')


    plt.xlabel('Return weighting methods', fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    new_labels = ['Equally weighted', 'Capped value weighted', 'Value weighted']
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels)

    plt.savefig(os.path.join('08_visualizations','agp_boxplot_return_weighting_by_percentiles.png'), dpi=800, bbox_inches='tight')

# FURTHER SEGMENTATION BY LBP-LENGTH
elif segmentation == 'lbp_length':
    # Starting the figure
    plt.figure(figsize=(10, 6))

    # Generating the box plot
    boxplot = sns.boxplot(data=df, x='ret_w', y='amount_of_months',
                          # Setting the whiskers to minimum and maximum
                          whis=(0, 100),
                          fill=True,
                          medianprops={'color': 'black', 'linewidth': 1},
                          linecolor='black',
                          linewidth=1,
                          # Further segmenting the results by LBP-length.
                          hue='lbp_length',
                          legend='full'
                          )

    plt.legend(title='LBP-length')

    plt.xlabel('Return weighting methods', fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    new_labels = ['Equally weighted', 'Capped value weighted', 'Value weighted']
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels)

    plt.savefig(os.path.join('08_visualizations','agp_boxplot_return_weighting_by_lbp_length.png'), dpi=800, bbox_inches='tight')