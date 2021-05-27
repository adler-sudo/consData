# -*- coding: utf-8 -*-
"""
Created on Tue May 25 21:18:50 2021

@author: james
"""

import tarfile
import os.path
import glob


# define today for file naming
today = '05252021'

# define dir
os.chdir('<directory>/genomic_coords_{}/genomic_coords_{}_simplified'.format(today,today))
  
# establish tracker
counter = 0

# write
tar = tarfile.open("consScores{}.tar.gz".format(today), "w:gz")
for file in os.listdir('./consData'):
    tar.add('/'.join([os.getcwd(),'consData',file]))
    counter += 1
tar.close()

# display number of files packed
print(counter,'files packed to tar.gz')
