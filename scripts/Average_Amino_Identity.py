#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import pandas as pd

def remove_files(files_in_cwd):
	for file in files_in_cwd:
		if ("tmp.aai." in file):
			os.remove(file)

def create_parser():
	parser = argparse.ArgumentParser(description="This program returns Average Amino Identity Coverage, Score, and Similarity for a one way blast to STDOUT. Other metrics are \
			displated as well. They are in the following order: Sum Amino Percent Match, Number of Total Fragments Matched, Query Sequence Match, Reference Sequence Match, \
			Coverage, Score, and Similarity")
	parser.add_argument("-q", "--query", dest="query", type=str, nargs=1 , help="Input is coding sequence file (.faa).", required=True)
	parser.add_argument("-r", "--reference", dest="reference", type=str, nargs=1, help="Reference nucleotide file (.fna).", required=True) 
	args = parser.parse_args()
	return args

def concatenate(input):
	seq = ''
	length = 0
	for line in open(input, 'r'):
		if (">" not in line):
			length += len(line.strip('\n'))
			seq += line.strip('\n')
	return seq, float(length)

def main():

	myargs = create_parser()
	query = myargs.query[0]
	reference = myargs.reference[0]

	number_of_fragments = 0
	for line in open(query, 'r'):
		if ('>' in line):
			number_of_fragments += 1

	rseq, rlength = concatenate(reference)

	make_blast_db = ["makeblastdb", "-in", reference, "-dbtype",  "prot", "-out", "tmp.aai.reference.db"]
	subprocess.call(make_blast_db)
	blast = ["blastp",  "-query", query, "-db", "tmp.aai.reference.db", "-out", "tmp.aai.blast.out", "-outfmt", '6 qseqid qlen qstart qend sseqid slen sstart send length nident mismatch gaps score bitscore evalue pident']
	subprocess.call(blast)

	blast_dataframe = pd.read_csv("tmp.aai.blast.out", sep="\t", header=None)
	blast_dataframe = blast_dataframe.drop_duplicates(subset=[blast_dataframe.columns[0]])

	qseq_length = 0
	#bnumber_of_fragments = 0
	sum_amino_percent_match = 0
	#rseq_length = 0
	for i in range(len(blast_dataframe)):
		#print blast_dataframe.iloc[i::+1, 8].values[0], blast_dataframe.iloc[i::+1, 9].values[0]
		amino_percent_match = float(blast_dataframe.iloc[i::+1, 9].values[0]) / float(blast_dataframe.iloc[i::+1, 8].values[0])
		#print amino_percent_match, blast_dataframe.iloc[i::+1, 15]
		if (amino_percent_match > 0.70 and blast_dataframe.iloc[i::+1, 15].values[0] > 0.70):
			sum_amino_percent_match += amino_percent_match
			qseq_length += blast_dataframe.iloc[i::+1, 8].values[0]
			#rseq_length += blast_dataframe.iloc[i::+1, 8].values[0]
			#bnumber_of_fragments += 1

	score = ((sum_amino_percent_match / number_of_fragments ) ) * 100
	coverage = (qseq_length / rlength) * 100
	similarity = coverage * score / 100

	print
	print sum_amino_percent_match, "\t", number_of_fragments, "\t", qseq_length, "\t", rlength, "\t", coverage, "\t", score, "\t", similarity
	print

	files_in_cwd = os.listdir(os.getcwd())
	remove_files(files_in_cwd)

if __name__ == "__main__":
	main()
