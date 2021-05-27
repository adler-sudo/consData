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
from pathlib import Path
import pandas as pd


# define today for writing unique files
today = '05252021'

# change working directory
os.chdir('<directory>/genomic_coords_{}/genomic_coords_{}_simplified/consData'.format(today,today))

# define directory of interest
directory = '.'

# define dataframe columns
columns = ['chr','start','stop','conservation_score']

# initiate master dataframe
masterdf = pd.DataFrame(columns=columns)

# loop through each file in the ConservationData_phyloP folder
for file in os.listdir():

  # create new dataframe for each file
  df = pd.DataFrame(columns=columns)
  
  # define full path
  file = '/'.join([directory,file])

  # open each file, read through lines, and grab info
  with open(file) as f:
    print(file)
    lines = f.readlines()

    for l in lines:
      print(l)
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
  

filename = Path('/'.join([os.getcwd(),'consDataByBase{}.tsv'.format(today)]))
print(filename)

# write to csv
if not filename.exists():
    masterdf.to_csv(filename,index=False, sep='\t')
