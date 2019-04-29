#!/usr/bin/env python3

import argparse
import sys

def create_parser():
	parser = argparse.ArgumentParser(description="This fragments a nucleotide sequence to 1000 base seuqnces.")
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input query file.", required=True)
	parser.add_argument("-out", dest="output", type=str, nargs=1, help="Name of the output filename.", required=True) 
	args = parser.parse_args()
	return args

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

	myargs = create_parser()
	query = myargs.input[0]
	#reference = sys.argv[2]
	outfile = myargs.output[0]

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

