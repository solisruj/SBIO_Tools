#!/usr/bin/python 

import sys
import subprocess
import os

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
	query = sys.argv[1]
	reference = sys.argv[2]
	outfile = sys.argv[3]

	make_blast_db = ["makeblastdb", "-in", reference, "-dbtype",  "nucl", "-out", "tmp.reference.db"]
	subprocess.call(make_blast_db)
	blast = ["blastn",  "-query", query, "-db", "tmp.reference.db", "-out", "tmp.blast.out",  "-outfmt", '6 qsedid qlen qstart qend seqid slen sstart send qseq sseq length nident mismatch gaps score bitscore evalue']
	subprocess.call(blast)

	files_in_cwd = os.listdir(os.getcwd())
	top_seq = get_top_seq_hit()
	formated_seq = Formatting_to_Fasta(top_seq)
	remove_files(files_in_cwd)
	write_out_file(formated_seq, outfile, query)

if __name__ == '__main__':
	main()


