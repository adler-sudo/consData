# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 00:10:36 2021

@author: james
"""


"""combine the conservation score data for region of interest and 
two flanks. plot on a strip plot to visualize the difference
"""

# import necessary modules
import pandas as pd
import os


# define dir
directory = 'C:/Users/james/rbpBiohack/'

os.chdir(directory)

# import each dataset
file1 = 'high_val_genome_coords/high_val_genome_coords_cons/highValGenomeCoordsConservationSummaryData.tsv'
df1 = pd.read_csv(file1,
                 sep='\t')
df1['group'] = 'high_val_genome_coords'


file2 = 'flank_before_table_browser/flank_before_reduced_cons/flankBeforeConservationSummaryData.tsv'
df2 = pd.read_csv(file2,
                  sep='\t')
df2['group'] = 'flank_before'


file3 = 'flank_after_table_browser/flank_after_reduced_cons/flankAfterConservationSummaryData.tsv'
df3 = pd.read_csv(file3,
                  sep='\t')
df3['group'] = 'flank_after'

# concat the dfs
masterdf = pd.concat([df1, df2, df3])

# THIS MAY NEED TO BE MOVED TO A DIFFERENT FILE
# stripplot
import seaborn as sns
import matplotlib.pyplot as plt

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
sns.violinplot(ax=ax, data=masterdf, x='group', y='averageConservationScore')
sns.stripplot(ax=ax, data=masterdf, x='group', y='averageConservationScore').set_title('Average Conservation Score by Group')