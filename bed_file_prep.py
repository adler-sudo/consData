# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 20:59:28 2021

@author: james
"""

"""reduces large .bed file down to 1000-row chunks so that
each portion of the .bed file can be individually submitted
to the UCSC genome browser"""

# import modules
import pandas as pd
import os


# set working directory
os.chdir('C:/Users/james/rbpBiohack/flank_after_table_browser')


# define and read in file
file = 'C:/Users/james/rbpBiohack/flank_after_table_browser/flank_after.bed'
df = pd.read_csv(file,
                 sep='\t',
                 header=None,
                 usecols=[0,1,2,3])

# split dataframe into 1000-row chunks
chunksize = 1000
for start in range(0,len(df),chunksize):
    print(start)
    subset_df = df.iloc[start:start + chunksize]
    subset_df.to_csv('flank_after_reduced_{}.bed'.format(start),
                     sep='\t',
                     header=None,
                     index=False)
