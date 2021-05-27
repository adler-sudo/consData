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
directory = <directory>

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

# TODO: THIS MAY NEED TO BE MOVED TO A DIFFERENT FILE
# stripplot
import seaborn as sns
import matplotlib.pyplot as plt

a4_dims = (30,17)
fig, ax = plt.subplots(figsize=a4_dims)
ax.set_ylabel('filler',fontsize=30)
ax.set_xlabel('filler',fontsize=30)
ax.set_xticklabels('filler', fontsize=25)
sns.violinplot(ax=ax, data=masterdf, x='group', y='averageConservationScore')
sns.stripplot(ax=ax, data=masterdf, x='group', y='averageConservationScore').set_title('Average Conservation Score by Group',fontsize=35)




# TODO: MOVE THIS TO A DIFFERENT FILE TOO!
# summary stats
masterdf.groupby('group').describe()['averageConservationScore']



# TODO: MOVE THIS TO DIFFERENT FILE TOO!
# t test
from scipy.stats import ttest_ind


ttest = ttest_ind(df1.averageConservationScore,
          df3.averageConservationScore,
          equal_var=False,
          alternative='greater')





# TODO: MOVE THIS TOO!
# create displot to visualize where high_val_genome coords are more \ 
    # highly represented
sns.displot(masterdf[['averageConservationScore','group']],
            x='averageConservationScore',
            hue='group')




# TODO: MOVE THIS TOO!
# create replicates and analyze distribution
# import modules
import numpy as np
import matplotlib.pyplot as plt


# initiate empty lists
highValReplicateMeans = []
flankBeforeReplicateMeans = []
flankAfterReplicateMeans = []


# generate replicates
np.random.seed(100)

for num in range(100):
    highValRep = [np.random.choice(df1.averageConservationScore) for _ in df1.averageConservationScore]
    highValReplicateMeans.append(np.mean(highValRep))
    
for num in range(100):
    flankRep = [np.random.choice(df2.averageConservationScore) for _ in df2.averageConservationScore]
    flankBeforeReplicateMeans.append(np.mean(flankRep))

for num in range(100):
    flankRep = [np.random.choice(df3.averageConservationScore) for _ in df3.averageConservationScore]
    flankAfterReplicateMeans.append(np.mean(flankRep))
    
    
# plot the distriubtions for the new replicate lists
plt.hist(highValReplicateMeans,color='green',label='high_val_reps')
plt.hist(flankBeforeReplicateMeans,label='flank_before_reps',color='blue')
plt.hist(flankAfterReplicateMeans,label='flank_after_reps',color='yellow')
plt.xlabel('averageRepConservationScore')
plt.ylabel('count')
plt.title('Replicate Histograms by Average Conservation Score')
plt.legend()
plt.show()
