#!/usr/bin/python

#!/usr/bin/python3
import os
import sys
import subprocess
import pandas as pd

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
	query = sys.argv[1]
	reference = sys.argv[2]
	#outfile = sys.argv[2]
	#query = './GCF_000006745.1_ASM674v1_genomic.fna'

	qseq, qlength= concatenate(query)
	qfragments = fragment(qseq)
	qcount = create_fragment_file(qfragments, 'tmp.ani.query.fragments.fna')

	rseq, rlength = concatenate(reference)
	rfragments = fragment(rseq)
	rcount = create_fragment_file(rfragments, 'tmp.ani.reference.fragments.fna')

	make_blast_db = ["makeblastdb", "-in", reference, "-dbtype",  "nucl", "-out", "tmp.ani.reference.db"]
	subprocess.call(make_blast_db)
	#blast = ["blastn",  "-query", 'tmp_fragments.fna', "-db", "tmp.reference.db", "-out", "tmp.blast.out",  "-outfmt", '6 qseqid qlen qstart qend sseqid slen sstart send qseq sseq length nident mismatch gaps score bitscore evalue']
	blast = ["blastn",  "-query", 'tmp.ani.query.fragments.fna', "-db", "tmp.ani.reference.db", "-out", "tmp.ani.blast.out",  "-outfmt", '6 qseqid qlen qstart qend sseqid slen sstart send length nident mismatch gaps score bitscore evalue']
	subprocess.call(blast)

	blast_output_dataframe = pd.read_table("tmp.ani.blast.out", sep="\t", header=None)
	blast_output_dataframe = blast_output_dataframe.drop_duplicates(subset=[blast_output_dataframe.columns[0]])
	#print blast_output_dataframe.head()
	frag_numbers = float(len(blast_output_dataframe))
	
	identity = float(blast_output_dataframe[9].sum())

	coverage = (identity / rlength ) * 100

	fragment_identities = 0
	for i in range(len(blast_output_dataframe)):
		#print blast_output_dataframe.iloc[i::+1, 8].values[0], blast_output_dataframe.iloc[i::+1, 9].values[0]
		frag_identity = float(blast_output_dataframe.iloc[i::+1, 9].values[0]) / float(blast_output_dataframe.iloc[i::+1, 8].values[0])
		fragment_identities += frag_identity

	score = ((fragment_identities / frag_numbers ) ) * 100

	similarity = coverage * score / 100

	print 
	print coverage, "\t", score, "\t", similarity
	print

	files_in_cwd = os.listdir(os.getcwd())
	remove_files(files_in_cwd)

if __name__ == '__main__':
	main()
