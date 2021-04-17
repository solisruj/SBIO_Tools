#!/usr/bin/env python3

import argparse
import os
import sys


def create_parser():
	parser = argparse.ArgumentParser(description="This program separates a concatenated fasta file into it sub sequences.")
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input fasta file.", required=True)
	args = parser.parse_args()
	return args

def write_sequences(input_file):
	header = None
	for line in open(input_file, 'r'):
		if '>' in line:
			header = line[1:].strip('\n')
			filename = header+'.fasta'
			outfile = open(filename, 'w')
			outfile.write('>'+header+'\n')
		else:
			sequence = line
			outfile.write(sequence)

def main():

	myargs = create_parser()
	input_file = myargs.input[0]
	write_sequences(input_file)

if __name__ == '__main__':
	main()