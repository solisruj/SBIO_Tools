#!/usr/bin/python3

import sys

def concatenate(input):
	seq = ''
	for line in open(input, 'r'):
		if (">" not in line):
			seq += line.strip('\n')
	return seq 

def Formatting_to_Fasta(seq):
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

def main():
	query = sys.argv[1]
	#reference = sys.argv[2]
	outfile = sys.argv[2]

	#query = './GCF_000006745.1_ASM674v1_genomic.fna'
	seq = concatenate(query)
	fragments = fragment(seq)

	count = 1
	output = open(outfile, 'w')
	for frag in fragments:
		output.write(">Fragment_" + str(count) + "\n")
		formatted_seq = Formatting_to_Fasta(frag.strip("\n"))
		for seq in formatted_seq:
			output.write(seq)
		count += 1

if __name__ == '__main__':
	main()

