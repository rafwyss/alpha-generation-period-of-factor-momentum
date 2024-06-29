import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Data visualization Python-Script Nr. 8.1.1
********************************************************************
BOX PLOT FOR AGP RESULTS 1971-2021 SEGMENTED BY PERCENTILES
********************************************************************
This file allows the generation of box plots of AGP results over 
the entire period from 1971 to 2021, segmented by percentiles.
The file also allows for further segmentation by LBP-lengths.
"""

"""IMPORTANT: CODE ONLY WORKS IF THERE IS A 'agp_{}_vert.csv' FILE WITH THE SPECIFIED WEIGHTING METHOD, AND INCLUDING 
THE SPECIFIED LBP-LENGTHS AND AMOUNT OF FACTORS IN THE '02-AGP-calculation' DIRECTORY"""

# Specify the segmentation.
# Options: For no further segmentation: 'none'. For further segmentation by LBP-lengths: 'lbp_length'.
segmentation = 'lbp_length'

# Choose a return weighting method
# Options: 'vw_cap', 'vw', 'ew'
ret_w = 'vw_cap'

# Importing the relevant data
df = pd.read_csv(os.path.join('..', '02_AGP-calculation',f'agp_{ret_w}_vert.csv'))


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
    boxplot = sns.boxplot(data=df, x='amount_of_factors', y='amount_of_months',
                # Setting the whiskers to minimum and maximum
                whis = (0,100),
                fill=True,
                medianprops = {'color':'black', 'linewidth':1},
                linecolor='black',
                linewidth=1,
                #order=['51', '30', '15', '7']
                )

    colors = ['#e8d4d0', '#d6aeb4', '#9d6b8a', '#473252']

    for i, patch in enumerate(boxplot.patches):
        face_color = colors[i % len(colors)]
        patch.set_facecolor(face_color)

    labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']
    plt.xticks(ticks=range(len(labels)), labels=labels)


    plt.xlabel('Percentiles', fontsize = 14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize = 14, fontweight='semibold',)

    medians = df.groupby(['amount_of_factors'])['amount_of_months'].median().values
    #medians[0], medians[1], medians[2] , medians[3]= medians[3], medians[2], medians[1], medians[0]
    means = df.groupby(['amount_of_factors'])['amount_of_months'].mean().values
    #means[0], means[1], means[2], means[3] = means[3], means[2], means[1], means[0]
    max_vals = df.groupby(['amount_of_factors'])['amount_of_months'].max().values
    #max_vals[0], max_vals[1], max_vals[2], max_vals[3] = max_vals[3], max_vals[2], max_vals[1], max_vals[0]


    for i, group in enumerate(df['amount_of_factors'].unique()):
        median = medians[i]
        mean = means[i]
        max_val = max_vals[i]

        # Adjusting the positioning
        if i == 0:
            j = -4
            place = 'top'
        else:
            j = 1
            place = 'bottom'

        plt.text(i, median + j, f'{median}', horizontalalignment='center', va=place,
                 color='black', weight='semibold', fontsize=11)

        plt.text(i, max_val, f'{max_val}', horizontalalignment='center', va='bottom',
                 color='black', weight='light', fontsize=11)


    plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_percentiles_{ret_w}.png'), dpi=800, bbox_inches='tight')


# FURTHER SEGMENTATION BY LBP-LENGTH
elif segmentation == 'lbp_length':
    # Starting the figure
    plt.figure(figsize=(10, 6))

    # Generating the box plot
    boxplot = sns.boxplot(data=df, x='amount_of_factors', y='amount_of_months',
                          # Setting the whiskers to minimum and maximum
                          whis=(0, 100),
                          fill=True,
                          medianprops={'color': 'black', 'linewidth': 1},
                          linecolor='black',
                          linewidth=1,
                          # order=['51', '30', '15', '7']
                          # Further segmenting the results by percentiles.
                          hue='lbp_length',
                          legend='full'
                          )

    handles, labels = boxplot.get_legend_handles_labels()
    labels = ['Top 5%', 'Top Decile', 'Top Quintile', 'Top Tercile']  # Custom labels
    plt.legend(handles, labels, title='LBP-length')

    plt.xticks(ticks=range(len(labels)), labels=labels)

    plt.legend(title='LBP-length')


    plt.xlabel('Percentiles', fontsize=14, fontweight='semibold', )
    plt.ylabel('Alpha-generation period [in months]', fontsize=14, fontweight='semibold', )

    plt.savefig(os.path.join('08_visualizations',f'agp_boxplot_percentiles_{ret_w}_by_lbp_length.png'), dpi=800, bbox_inches='tight')