#!/usr/bin/env python3

# Importing modules.
import pandas as pd
import argparse

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program provides the complementary sequence to a DNA strand of intereset.")
	parser.add_argument("-in", "--input_fasta", dest="input_fasta", type=str, nargs=1 , help="Input fasta file. This can be an assembly, or sequence in base format.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output complementary fasta/sequence file.", required=True) 
	args = parser.parse_args()
	return args

# This function reads in the file and loads the information into a dictionary.
def sequence_to_dictionary(file_name):
	sequence_dict = {}
	with open(file_name) as f:
		for line in f.readlines():
			#print line.strip('\n')
			if('>' in line):
				header = line
				sequence = ''
			if('>' not in line):
				fragement = line
				sequence += fragement.strip('\n')
			sequence_dict[header] = sequence[::-1]
	return sequence_dict

# This function gets the DNA complementary strand of the DNA and writes it to an outfile. 
def DNA_to_Complementary(sequences_dict, outfile):
	complementary_sequence = ''
	output_file = open(outfile, 'w')
	for header in sequences_dict:
		output_file.write(header)
		for base in sequences_dict[header]:
			if(base == 'A'):
				complementary_sequence += 'T'
			elif(base == 'T'):
				complementary_sequence += 'A'
			elif(base == 'C'):
				complementary_sequence += 'G'
			elif(base == 'G'):
				complementary_sequence += 'C'
		formatted_sequence = Formatting_to_Fasta(complementary_sequence)
		for seq in formatted_sequence:
			output_file.write(seq)
	output_file.close()

# Formats a string into a list of sequence of length 70, and returns the list.
def Formatting_to_Fasta(seq):
	sequence_fasta_format = []
	for n in xrange(0,len(seq), 70):
		line = str(seq[n:n+70])+"\n"
		sequence_fasta_format.append(line)
	return sequence_fasta_format

# Main body of the program.
def main():
	myargs = create_parser()
	input_file = myargs.input_fasta[0]
	out_file = myargs.output_file[0]
	sequence_dict = sequence_to_dictionary(input_file)
	DNA_to_Complementary(sequence_dict, out_file)

if __name__ == '__main__':
	main()


