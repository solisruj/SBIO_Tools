#!/usr/bin/env python3

# Importing modules.
import argparse

# Function to parse command-line arguments.
def create_parser():
	parser = argparse.ArgumentParser(description="Transcribes an input DNA sequence to RNA.")
	parser.add_argument("-in", "--input_fasta", dest="input_fasta", type=str, nargs=1 , help="Input fasta file. This can be an assembly, or sequence in base format.", required=True)
	parser.add_argument("-out", "--output_fasta", dest="output_fasta", type=str, nargs=1, help="Name of the output file containing the transcribed sequence.", required=True) 
	args = parser.parse_args()
	return args

# This function transcribes the sequence to RNA as the input file is read. It also write the RNA sequence to an output file.
def transcribe_DNA_to_RNA(file_name, outfile):
	with open(file_name) as f:
		output_file = open(outfile, 'w')
		for line in f.readlines():
			if('>' in line):
				output_file.write(line)
				sequence = ''
			if('>' not in line):
				fragement = line
				fragement = fragement.replace('T', 'U').strip('\n')
				sequence += fragement
		formatted_fragment = Formatting_to_Fasta(sequence)
		for line in formatted_fragment:
			output_file.write(line)
	output_file.close()

# This fucntion formats a sequence into a list of line sequences 70 bases long.
def Formatting_to_Fasta(seq):
	sequence_fasta_format = []
	for n in xrange(0,len(seq), 70):
		line = str(seq[n:n+70])+"\n"
		sequence_fasta_format.append(line)
	return sequence_fasta_format

# Main body of the program.
def main():
	myargs = create_parser()
	in_file = myargs.input_fasta[0]
	out_file = myargs.output_fasta[0]
	transcribe_DNA_to_RNA(in_file, out_file)

if __name__ == '__main__':
	main()



