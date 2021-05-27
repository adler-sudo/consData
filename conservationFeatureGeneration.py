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
from pathlib import Path


# define today for unique file writing
today = '05252021'

# set directory MERIDITH
os.chdir('C:/Users/james/rbpBiohack/genomic_coords_{}/genomic_coords_{}_simplified/consData'.format(today,today))

# set directory LESLIE
# os.chdir('C:/Users/james/openASO/Both_ASO_siRNA_BlastResults/consData')


# read in the conservation data
file = 'consDataByBase{}.tsv'.format(today)
conservationData = pd.read_csv(file,sep='\t')
conservationData['chr'] = 'chr' + conservationData['chr']

# read in site locations file
df = pd.read_csv('../all_exons.bed',
                 sep='\t',
                 usecols=[0,1,2,3],
                 header=None)
df.columns = ['chrom','chromStart','chromEnd','regionName']
df['chromStart'] = df.chromStart + 1
df.sort_values(by='chromStart',inplace=True)
df.reset_index(drop=True,inplace=True)

# establish average score and count above 0 columns
# DIDN'T NEED THIS FOR MOST RECENT PROJECT FOR MERIDITH
# TODO: add this to an option of the class/function
# df['averageConservationScore'] = 0
# df['countConserveAboveZero'] = 0



# CODE FROM 05252021 (MAY MAKE SENSE TO TURN THIS INTO FUNCTION OR OWN FILE)
# have to add another step here for bringing exons back together \
    # that we split due to regions spanning multiple exons

# create column to identify exons from same original file
df['fromFile'] = df.regionName.apply(lambda x: x[:-1])

# loop through unique files and collect cons data for each nucleotide
unique_files = df.fromFile.unique()

for file in unique_files:
    
    # filter for exons for each file
    file_df = df.loc[df.fromFile == file]
    print('there are {} exons in this file'.format(len(file_df)))
    
    # initate empty cons dataframe
    ss = pd.DataFrame(columns = conservationData.columns)
    
    # for each exon associated with the file, grab cons data
    for _, exon in file_df.iterrows():
        
        
        # TODO: we could still be grabbing unwanted data here if we have alternative \
            # TODO: splicing, but should be just fine for now
        # grab cons data
        sub_df = conservationData.loc[(conservationData.start >= exon.chromStart) & (conservationData.stop <= exon.chromEnd) & (conservationData.chr == exon.chrom)]
        
        # add filename for back reference
        sub_df['fileName'] = file
        
        # add individual exon cons data to ss
        ss = pd.concat([ss,sub_df])
    
    # drop duplicates since some exons were represented in mulitple files
    ss.drop_duplicates(subset='start',inplace=True)
    
    # define filename and write if it doesn't exist
    filename = Path('{}_consScore.bed'.format(file_df.fromFile.iloc[0,][:-4]))
    
    if not filename.exists():
        ss.to_csv(filename,sep='\t',index=False,header=False)
        print('{} created'.format(filename))
    else:
        print('{} already exists'.format(filename))





# COMMENTED OUT FOR 05252021
# # loop through each ASO
# for i in range(len(df)):
#   print(i)

#   # subset for conservation data in the nucleotide range for the ASO binding site
#   ss = conservationData.loc[(conservationData.start >= df.loc[i,'chromStart']) & (conservationData.stop <= df.loc[i,'chromEnd'])]
#   filename = Path('./{}_{}-{}_consScore'.format(ss.chr.iloc[0],ss.start.min(),ss.stop.max())+'.bed')
  
#   if not filename.exists():
#       ss.to_csv(filename,sep='\t',index=False,header=False)
#   else:
#       print(filename,'already exists')
#   # MERIDITH ^^^^
  
  
  
  
# # BELOW HERE WASN'T NEED FOR MOST RECENT PROJECT ON 05/04
#   # if there is matching data
#   if len(ss) > 0:

#     # get the average score
#     df.loc[i,'averageConservationScore'] = ss.conservation_score.mean()

#     # get the count above 0
#     df.loc[i, 'countConserveAboveZero'] = (ss.conservation_score > 0).sum()
    
# # TODO: MISSED 1ST 1000 ROWS FOR SOME REASON ON FLANK AFTER
# # TODO: SEE IF THIS OCCURRED FOR THE OTHER ONES TOO ^
# # write to tsv
# df.to_csv('consDataByExon{}.tsv'.format(today), sep='\t', index=False)