from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.axes import Axes
import HTSeq
import pandas as pd
import itertools
import argparse
import os


parser = argparse.ArgumentParser(
        description="""
        This is written for Python 2.x. And requires several libraries as seen on top of the script.
        The main purpose of the program is to generate a dataframe from PacBio fastq.gz files,
        that includes.
        Check how 'os.walk' works in case it doesn't work for you. 
         """)

parser.add_argument('INDIR', help="Full Path to directory that contains all fasta/q files", type=str)
parser.add_argument('OUTFILE', help="OUTFILE name", type=str)
parser.add_argument('FILE_TYPE', help="fasta or fastq", type=str)

args = parser.parse_args()
fastq_folder = args.INDIR
out = args.OUTFILE
file_type = args.FILE_TYPE

#get the filenames using listdir now
file_handler = os.listdir(fastq_folder)


#this changed with initiating git.
files = [x for x in file_handler if file_type in x]


#this initiates the variables saved in the final dataframe/csv file
read_length_ind = []
read_name_ind = []
read_origin = []


#sets working directory
os.chdir(fastq_folder)

#counter for number of proccessed files
count = 0

# for each .gz file, that is read in and three lists are produced
for file in files:
    if 'fastq' == file_type:
        fastq_ind = HTSeq.FastqReader(file, "solexa")
    elif 'fasta' == file_type:
        fastq_ind = HTSeq.FastaReader(file)
    else:
        print("Please indicate file format fasta or fastq")
    for read in fastq_ind:
        read_name_ind.append(read.name)
        read_length_ind.append(len(read))
        read_origin.append(x)
    count += 1
    print('Done %s. %d out of %d more to go.' %(x, (len(gz_files_list)- count), len(gz_files_list)))
s3 = pd.Series(read_length_ind, name='read_length')
s4 = pd.Series(read_name_ind, name='read_name')
s5 = pd.Series(read_origin, name='read_origin')
df_ind = pd.concat([s3, s4, s5], axis=1)


#sort the df and do cumsum
df_ind_sorted = df_ind.sort_values(by='read_length')
df_ind_sorted['CS_length']=df_ind_sorted['read_length'].cumsum()


df_ind_sorted.to_csv(out+'.csv', encoding='utf-8')
