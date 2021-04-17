# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 23:10:44 2021

@author: james
"""

"""
cross-reference phylo data with locations of interest .bed file
in order to pull information for each of the regions

here, we specifically grab the mean and the number
of sites that are above zero (these are the two pieces of
                              data that had interested leslie,
                              so that's why they are here)
"""

# import modules
import pandas as pd
import os


# set directory
os.chdir('C:/Users/james/rbpBiohack/flank_after_table_browser/flank_after_reduced_cons')

# read in the conservation data
file = 'phyloDataFlankAfter04162021.tsv'
conservationData = pd.read_csv(file,sep='\t')

# read in site locations file
df = pd.read_csv('../flank_after.bed',
                 sep='\t',
                 usecols=[0,1,2,3],
                 header=None)
df.columns = ['chrom','chromStart','chromEnd','id']

# establish average score and count above 0 columns
df['averageConservationScore'] = 0
df['countConserveAboveZero'] = 0

# loop through each ASO
for i in range(len(df)):
  print(i)
  
  # subset for conservation data in the nucleotide range for the ASO binding site
  ss = conservationData.loc[(conservationData.start >= df.chromStart[i]) & (conservationData.start <= df.chromEnd[i])]
  
  # if there is matching data
  if len(ss) > 0:

    # get the average score
    df.loc[i,'averageConservationScore'] = ss.conservation_score.mean()

    # get the count above 0
    df.loc[i, 'countConserveAboveZero'] = (ss.conservation_score > 0).sum()
    
# TODO: MISSED 1ST 1000 ROWS FOR SOME REASON ON FLANK AFTER
# TODO: SEE IF THIS OCCURRED FOR THE OTHER ONES TOO ^
# write to tsv
df.to_csv('flankAfterConservationSummaryData.tsv', sep='\t', index=False)