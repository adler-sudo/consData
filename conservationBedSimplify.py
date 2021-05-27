# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:44:21 2021

@author: james
"""


"""
input: folder of bed files of single exons broken down into individual \
    nucleotides
    
output: all exons consolidated to one bed file

used this for the genomic coordintes sent on 5/4 for rbpbiohack
"""

# import necessary modules, as always
import pandas as pd
import os
import glob


# define today for unique file naming
today = '05252021'

# set working directory
os.chdir('C:/Users/james/rbpBiohack/genomic_coords_{}'.format(today))

# destination directory
directory = 'C:/Users/james/rbpBiohack/genomic_coords_{}/genomic_coords_{}_simplified'.format(today,today)

# empty master dataframe
master_df = pd.DataFrame()

# keep track of number of files
numFiles = 0

# loop through each file
for file in glob.glob('*.bed'):
    
    numFiles+=1
    
    # determine chrom, start, and stop for exon
    df = pd.read_csv(file,sep='\t',usecols=[0,1,2],header=None)
    df.columns = ['chrom', 'start', 'end']
    df.sort_values(by='start',inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    # define continuous regions
    # eliminates includsion of introns (some bed files span multiple exons)
    smallNuc = df.start.min()
    largeNuc = df.end.max()
    numberNuc = len(df)
    
    # defined numExons to be used for indexing and naming
    numExons = 1
    
    if (int(largeNuc) - int(smallNuc)) == numberNuc:
        print('just 1 exon in file')
        chrom = df.chrom[0]
        start = smallNuc - 1 # TODO: we may need to subtract 1 from this start location due to table browser
        end = largeNuc
    
        dfSingleExon = pd.DataFrame(
            data = {'chrom':[chrom],
                    'start':[start],
                    'end':[end],
                    'regionName':''.join([file,str(numExons)])})
        
        master_df = master_df.append(dfSingleExon)
    
    else:
        print('multiple exons in file')
        
        # determine location of splice junctions
        lastNuc = df.start[0]
        startNuc = df.start[0]
        
        for loc,nuc in enumerate(df.start[1:]):
            
            if nuc == (lastNuc + 1):
                lastNuc = nuc
            
            else:
                
                # add the previous exon and move to the next
                dfSingleExon = pd.DataFrame(
                    data = {'chrom':[df.chrom[0]],
                            'start':[startNuc-1],
                            'end':[lastNuc+1],
                            'regionName':''.join([file,str(numExons)])})
                
                master_df = master_df.append(dfSingleExon)
                    
                numExons += 1 # add 1 to exon counter
                
                print('splice junction at {}!'.format(loc))
                print('added previous exon to df, beggining new exon')
                print(df.start[0],'-',df.start[loc],df.start[loc+1],'-',df.start.iloc[-1,])
                
                startNuc = nuc # define new start nucleotide
                lastNuc = nuc
        
        # at the end of the loop, we will need to add the last exon
        dfSingleExon = pd.DataFrame(
                    data = {'chrom':[df.chrom[0]],
                            'start':[startNuc-1], # -1 accounts for indexing in UCSC
                            'end':[lastNuc+1],
                            'regionName':''.join([file,str(numExons)])}) # +1 accounts for we are need the value from end column
        
        master_df = master_df.append(dfSingleExon)
        
        
        print('there are {} exons in {}'.format(numExons,file))

print('{} files processed'.format(numFiles))
print('{} exons found'.format(len(master_df)))

# write the dataframe of exons to new consolidated bed
master_df.reset_index(drop=True,inplace=True)
master_df.to_csv('/'.join([directory,'all_exons.bed']),index=False,sep='\t',header=False)