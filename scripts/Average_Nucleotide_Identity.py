#!/usr/bin/python

#!/usr/bin/python3
import os
import sys
import subprocess
import argparse
import pandas as pd

def create_parser():
	parser = argparse.ArgumentParser(description="This program returns Average Nucleotide Identity Coverage, Score, and Similarity for a one way blast to STDOUT. Other metrics are \
			displated as well. They are in the following order: Sum Nucleotide Percent Match, Number of Total Fragments Matched, Query Sequence Match, Reference Sequence Match, \
			Coverage, Score, and Similarity")
	parser.add_argument("-q", "--query", dest="query", type=str, nargs=1 , help="Input nucleotide sequence file (.fna/.fasta).", required=True)
	parser.add_argument("-r", "--reference", dest="reference", type=str, nargs=1, help="Reference nucleotide file (.fna/.fasta).", required=True) 
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

def formatting_to_fasta(seq):
	sequence_fasta_format = []
	for n in range(0,len(seq), 70):
		line = str(seq[n:n+70])+"\n"
		sequence_fasta_format.append(line)
	return sequence_fasta_format

def fragment(seq):
	fragments = []
	for n in range(0,len(seq), 1000):
		line = str(seq[n:n+1000])+"\n"
		fragments.append(line)
	return fragments

def create_fragment_file(fragments, outfile_name):
	count = 1
	output = open(outfile_name, 'w')
	for frag in fragments:
		output.write(">Fragment_" + str(count) + "\n")
		formatted_seq = formatting_to_fasta(frag.strip("\n"))
		for seq in formatted_seq:
			output.write(seq)
		count += 1
	output.close()
	return count

def remove_files(files_in_cwd):
	for file in files_in_cwd:
		if ("tmp.ani." in file):
			os.remove(file)

def main():

	myargs = create_parser()
	query = myargs.query[0]
	reference = myargs.reference[0]

	qseq, qlength= concatenate(query)
	qfragments = fragment(qseq)
	qcount = create_fragment_file(qfragments, 'tmp.ani.query.fragments.fna')

	rseq, rlength = concatenate(reference)
	rfragments = fragment(rseq)
	rcount = create_fragment_file(rfragments, 'tmp.ani.reference.fragments.fna')

	make_blast_db = ["makeblastdb", "-in", reference, "-dbtype",  "nucl", "-out", "tmp.ani.reference.db"]
	subprocess.call(make_blast_db)
	blast = ["blastn",  "-query", 'tmp.ani.query.fragments.fna', "-db", "tmp.ani.reference.db", "-out", "tmp.ani.blast.out",  "-outfmt", '6 qseqid qlen qstart qend sseqid slen sstart send length nident mismatch gaps score bitscore evalue']
	subprocess.call(blast)

	blast_dataframe = pd.read_table("tmp.ani.blast.out", sep="\t", header=None)
	blast_dataframe = blast_dataframe.drop_duplicates(subset=[blast_dataframe.columns[0]])

	query_length = 0
	total_number_of_fragments = 0
	sum_percent_nucleotide_match = 0
	for i in range(len(blast_dataframe)):
		percent_nucleotide_match = float(blast_dataframe.iloc[i::+1, 9].values[0]) / float(blast_dataframe.iloc[i::+1, 8].values[0])
		if (percent_nucleotide_match > 0.70):
			sum_percent_nucleotide_match += percent_nucleotide_match
			query_length += blast_dataframe.iloc[i::+1, 9].values[0]
			total_number_of_fragments += 1

	score = ((sum_percent_nucleotide_match / total_number_of_fragments ) ) * 100
	coverage = (query_length / rlength ) * 100
	similarity = coverage * score / 100

	print 
	print sum_percent_nucleotide_match, "\t", total_number_of_fragments, "\t", query_length, "\t", coverage, "\t", score, "\t", similarity
	print

	files_in_cwd = os.listdir(os.getcwd())
	remove_files(files_in_cwd)

if __name__ == '__main__':
	main()
