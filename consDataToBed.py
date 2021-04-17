# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 22:16:43 2021

@author: james
"""


"""consolidates the individual 1000-row chunks from the 
UCSC table browser output into a single .tsv file that
can be used to grab conservation score data.
"""

# import modules
import os
import pandas as pd


# change working directory
os.chdir('C:/Users/james/rbpBiohack/flank_after_table_browser/flank_after_reduced_cons')

# create list of all conservation files
conservationFiles = os.listdir()

# initiate master dataframe
masterdf = pd.DataFrame(columns=['chr','start','stop','conservation_score'])

# define directory of interest
directory = '.'

# loop through each file in the ConservationData_phyloP folder
for file in conservationFiles:

  # create new dataframe for each file
  df = pd.DataFrame(columns=['chr','start','stop','conservation_score'])

  # define full path
  file = '/'.join([directory,file])

  # open each file, read through lines, and grab info
  with open(file) as f:
    print(file)
    lines = f.readlines()

    for l in lines:

      # grab chromosome number (changes for each 'sample')
      # NEED TO ACCOUNT FOR X CHROMOSOME
      if l.startswith('#'):

        chrom_finder = 'chrom specified: chr'

        if chrom_finder in l:
          ind = int(l.find(chrom_finder) + len(chrom_finder))
          chr = l[ind:].rstrip()

        # chr = regex.findall('\d+',l)[0]


      # if line starts with digit, grab location and conservation score
      if l[0].isdigit():
        l = l.rstrip()
        l = l.split('\t')
        start = l[0]
        conservation_score = l[1]

        # append new observation to dataframe
        newLine = {'chr':chr,'start':start,'stop':start,'conservation_score':conservation_score}
        df = df.append(newLine, ignore_index=True)
      
  masterdf = masterdf.append(df, ignore_index=True)
  print(masterdf.tail())
  
# write to csv
masterdf.to_csv('phyloDataFlankAfter04162021.tsv',index=False, sep='\t')