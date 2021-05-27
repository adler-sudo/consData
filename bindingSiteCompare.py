# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:32:18 2021

@author: james
"""


"""this file is used to asses binding site conservation score
relative to the rest of the exon

the predicted binding site for the rbpbiohack project is always
at the 50th-56th base in each of the regions of interest"""

import os
import glob
from pathlib import Path
import pandas as pd


# define today
today = '05252021'

# define exon to read
os.chdir('<directory>/genomic_coords_{}/genomic_coords_{}_simplified/consData/'.format(today,today))

# define binding site
bindStart = 50
bindEnd = 56

# define bind site df
bind_df = pd.DataFrame()

# loop through directory
for file in glob.glob('*.bed'):
    
    # read in the exon
    df = pd.read_csv(
        file,
        sep='\t',
        header=None)
    
    df.columns = ['chr','chrStart','chrEnd','conservationScore','fileName']
    
    # summary stats
    averageConsScore = df.conservationScore.mean()
    stdConsScore = df.conservationScore.std()
    
    # normalize scores
    df['normalizedConsScore'] = (df.conservationScore - averageConsScore) / stdConsScore
    
    # define our regions
    chrom = df.chr[0]
    start = df.chrStart.min()
    end = df.chrEnd.max()
    site50 = df.normalizedConsScore[bindStart-1]
    site51 = df.normalizedConsScore[bindStart]
    site52 = df.normalizedConsScore[bindStart+1]
    site53 = df.normalizedConsScore[bindStart+2]
    site54 = df.normalizedConsScore[bindStart+3]
    site55 = df.normalizedConsScore[bindStart+4]
    site56 = df.normalizedConsScore[bindStart+5]
    bindSiteMean = df.normalizedConsScore[bindStart-1:bindEnd].mean()
    fileName = df.fileName.iloc[0,]
    
    # consolidate to new dataframe
    dfSingleExon = pd.DataFrame(
        data = {'chrom':[chrom],
                'start':[start],
                'end':[end],
                'site50normConsScore':[site50],
                'site51normConsScore':[site51],
                'site52normConsScore':[site52],
                'site53normConsScore':[site53],
                'site54normConsScore':[site54],
                'site55normConsScore':[site55],
                'site56normConsScore':[site56],
                'normalizedBindSiteMean':[bindSiteMean],
                'originalFileName':[fileName]})
    
    # append to master df
    bind_df = bind_df.append(dfSingleExon)
    
    # binding site normalized score
    print('cons scores sites 50-56:',df.normalizedConsScore[bindStart-1:bindEnd].values)

print('{} regions normalized and binding sites calc\'d'.format(len(bind_df)))
   
# write the bind df to csv
filename = Path('bindSiteMeanSummary.tsv')
if not filename.exists():
    bind_df.to_csv(filename,sep='\t',index=False)

