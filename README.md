# The alpha-generation period of factor momentum strategies

This code was used in the Bachelor's Thesis.

This repository contains the Python code for the thesis "The alpha-generation period of factor momentum strategies". 

The repository is structured into a data preparation section, a section on the calculation of alpha-generation period results and lastly a section on the statistical analysis as well as results visualization.

## Content
### 1. Factor return data preparation

To start the analysis first execute the file "01_factor-return-data-preparation.py" to create a data frame containing only the relevant factor return data.

To get descriptive statistics on the relevant factor return data selected, execute "01a_factor-return-data-statistics.py".


### 2. Calculation of the Alpha-Generation Period

First, the total geometric returns over all specified look-back-periods (LBP) for all 153 factors are generated by executing "02_total-lbp-factor-returns.py".

Next, the total geometric factor returns over the specific LBPs are used to rank the factors in "03_factors-sorted-for-total-factor-returns.py".

Based on the ranking, factor momentum portfolios for the specific percentiles can be created and the monthly factor momentum portfolio returns starting one month after the end of the LBP can be computed in "04_sim-monthly-pf-returns.py".

The monthly factor momentum portfolio returns are then converted to trailing-twelve months factor momentum portfolio returns (TTM) in "05_sim-ttm-pf-returns.py".

Based on the TTM-portfolio returns, the alpha-generation period of the individual factor momentum portfolios is measured in "06_agp-analysis-vertical.py". Additionally, the data can be generated in a pivot table format by executing "06a_agp-analysis-pivot.py".


### 3. Statistical analysis of the AGP-results
The repository contains Python files to generate summary statistics, significance statistics and regression results as well as box plots, scatter plots.


#### Summary, significance and regression statistics
First, this repository contains code to generate summary statistics for the AGP results. 
"07_1_agp-summary-statistics.py" generates summary statistics for each model. 
"07_1a_agp-summary-statistics-excl.py" calculates the percentages of AGP results shorter than 12 or 24 months and generates summary statistics excluding those values.

File "07_2_agp-significance_statistics.py" can be used to generate significance statistics for all models, including hypothesis testing and confidence interval.

Files "07_3_agp-over-eras-summary-statistics.py", "07_4_agp-over-eras-significance-statistics.py" and "07_4a_agp-over-eras-significance-statistics-segmented-by-only-one-variable" can be used to generate significance statistics over multiple eras, generating insights into the development of the AGP.

Last, code for regression statistics can be used to generate categorical, dummy variable (and if possible linear) regression statistics. 
"07_05_1_regression-percentiles" regresses the AGP results on the percentile (amount of factors in the FM portfolio).
"07_05_2_regression-lbp-length" regresses the AGP results on the LBP-length used.
"07_05_3_regression-return-weighting" regresses the AGP results on the underlying factor return weighting method used.
"07_05_4_regression-over-eras" regresses the AGP results on different eras, during which they were computed.

#### Results visualization
To further assist with the understanding of the results, data visualization code is provided.

Box plots help understand the distribution of the AGP results. 
"08_1_1_agp-box-plot-percentiles" generates box plots segmented by different percentiles.
"08_1_2_agp-box-plot-lbp-length" generates box plots segmented by different LBP-lengths.
"08_1_3_agp_boxplots_ret_w" generates box plots segmented by different underlying factor return weighting method used.
"08_2_agp-box-plot-over-eras" generates box plots segmented by different eras, during which the AGP results were computed.


## Guidance
### Input parameters
Each script works with different input parameters. These are specified in lists at the top of the script, before the analyis.
To compute AGP results using only a set of these input parameters, COMMENT OUT the other parameters (don't delete them).

By default, results will be calculated for all percentiles and LBP-lengths, but only for capped value weighted underlying factor returns. To generate AGP results with other return weighting methods as well, uncomment them in each script.


