import os

"""
THE ALPHA-GENERATION-PERIOD OF OPTIMIZED FACTOR-INVESTING STRATEGIES
--------------------------------------------------------------------
Set-up Python-Script Nr. 0
********************************************************************
CREATING THE DIRECTORIES NECESSARY FOR THE CODE TO WORK
********************************************************************
"""

# 2. Total LBP factor returns
os.makedirs(os.path.join('..','02_AGP-calculation', '02_total-lbp-factor-returns'))
# 3. Factors ranked by total LBP factor returns
os.makedirs(os.path.join('..','02_AGP-calculation', '03_factors-ranked-by-total-factor-returns'))
# 4. Monthly factor momentum portfolio returns
os.makedirs(os.path.join('..','02_AGP-calculation', '04_sim-monthly-pf-returns'))
# 5. TTM factor momentum portfolio returns
os.makedirs(os.path.join('..','02_AGP-calculation', '05_sim-ttm-pf-returns'))
# 6. AGP pivot
os.makedirs(os.path.join('..','02_AGP-calculation', '06a_agp_pivot'))
# 7. Statistics
os.makedirs(os.path.join('..','03_statistical-analysis', '07_statistics'))
# 8. Visualizations
os.makedirs(os.path.join('..','03_statistical-analysis', '08_visualizations'))