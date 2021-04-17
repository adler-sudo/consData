# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 23:48:38 2021

@author: james
"""


"""builds flanking regions datasets before and after a set of regions of
interest. flanking regions are the same size as the region of interest.
"""

# import modules
import pandas as pd


# specify bed file from meridith
file = 'C:/Users/james/Downloads/high_val_genome_coords.bed'

# convert bed file to dataframe
df = pd.read_csv(file, sep='\t', header=None)
df.columns = ['chr', 'start', 'stop', 'id', 'fSCORE', 'strand']

# calc width of each location
section_width = df.stop - df.start

# identify flanking locations
flank_before = df.copy()
flank_before['start'] = df.start - section_width - 1
flank_before['stop'] = df.stop - section_width - 1

flank_after = df.copy()
flank_after['start'] = df.start + section_width + 1
flank_after['stop'] = df.stop + section_width + 1

# convert flanking regions to beds
# TODO: should we change the id name before writing them to new files?
flank_before.to_csv('flank_before.bed', sep='\t', index=False, header=False)
flank_after.to_csv('flank_after.bed', sep='\t', index=False, header=False)
