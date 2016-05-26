from Bio import SeqIO
import argparse


parser = argparse.ArgumentParser(
        description="""
        Splits up an input alternative contig file into a number of files chose.
        It also prints a bash script for commiting each blat search to the cluster.
         """)

parser.add_argument('INDIR', help="Full Path to directory that contains a_ctg file", type=str)
parser.add_argument('INFILE', help="In file name")
parser.add_argument('N', help="Number of output files. Equals number of jobs submitted to the cluster.", type=int)
parser.add_argument('REF', help="Name for ref fasta", type=str)
parser.add_argument('BASH', help="Name for bash file", type=str)


args = parser.parse_args()

#here is the in file defined containing alternative 
file_path = args.INDIR
file_name=args.INFILE
numbers_of_file = args.N
bash_script = args.BASH
ref_fasta = args.REF

#get total number of records in the file
total_seq_recs = 0
for seq_record in SeqIO.parse(file_path+'/'+file_name, "fasta"):
    total_seq_recs += 1

#caclculate additional records added to first file
add_seq_first_file = total_seq_recs%numbers_of_file


#caclculate records per file
sequences_in_file = total_seq_recs//numbers_of_file

#pull in all records
recs = []
for seq_record in SeqIO.parse(file_path+'/'+file_name, "fasta"):
    recs.append(seq_record)

#write first file
frist_file= '0_'+file_name
SeqIO.write(recs[0:(add_seq_first_file+sequences_in_file)], frist_file, 'fasta')
count = 0

#write start writing bash script
outf = open(bash_script, 'w')
outf.write('#!/bin/bash\n')
outf.write("qsub -cwd -b y -N blat_%s -pe threads 1 -l virtual_free=1G 'blat %s %s %s.psl'\n"%(str(count),ref_fasta, frist_file, frist_file))

#write remaining files and parts of the bash script
for x in range((add_seq_first_file+sequences_in_file), total_seq_recs, sequences_in_file):
    count += 1
    current_file = str(count)+'_'+file_name
    SeqIO.write(recs[x:(x+sequences_in_file)], current_file, 'fasta')
    outf.write("qsub -cwd -b y -N blat_%s -pe threads 1 -l virtual_free=1G 'blat %s %s %s.psl'\n"%(str(count),ref_fasta, current_file, current_file))

outf.close()




