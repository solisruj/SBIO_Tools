#!/usr/bin/env python3 

import argparse
import sys
import subprocess
import os

def create_parser():
	parser = argparse.ArgumentParser(description="This program extracts the hight similar sequence found in a reference that matches the query.")
	parser.add_argument("-q", dest="query", type=str, nargs=1 , help="Input query file.", required=True)
	parser.add_argument("-r", dest="reference", type=str, nargs=1 , help="Reference file.", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Name of the output filename.", required=True) 
	args = parser.parse_args()
	return args

def remove_files(files_in_cwd):
	for file in files_in_cwd:
		if ("tmp.reference.db" in file):
			os.remove(file)
		if ("tmp.blast.out" in file):
			os.remove(file)

def Formatting_to_Fasta(seq):
	sequence_fasta_format = []
	for n in xrange(0,len(seq), 70):
		line = str(seq[n:n+70])+"\n"
		sequence_fasta_format.append(line)
	return sequence_fasta_format

def get_top_seq_hit():
	rows = []
	count = 0
	for lines in open('tmp.blast.out', 'rb'):
		rows.append(lines.split('\t'))
		if (count > 1):
			break
		count += 1
	return rows[0][7]

def write_out_file(sequence, outfile, query):
	output = open(outfile, 'w')
	output.write(">" + query + '\n')
	for line in sequence:
		output.write(line)

def main():

	myargs = create_parser()
	query = myargs.query[0]
	reference = myargs.reference[0]
	outfile = myargs.output[0]

	make_blast_db = ["makeblastdb", "-in", reference, "-dbtype",  "nucl", "-out", "tmp.reference.db"]
	subprocess.call(make_blast_db)
	blast = ["blastn",  "-query", query, "-db", "tmp.reference.db", "-out", "tmp.blast.out",  "-outfmt", '6 qsedid qlen qstart qend seqid slen sstart send qseq sseq length nident mismatch gaps score bitscore evalue']
	subprocess.call(blast)

	files_in_cwd = os.listdir(os.getcwd())
	top_seq = get_top_seq_hit()
	formated_seq = Formatting_to_Fasta(top_seq.replace('-', ''))
	remove_files(files_in_cwd)
	write_out_file(formated_seq, outfile, query)

if __name__ == '__main__':
	main()


