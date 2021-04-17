#!/usr/bin/env python3


import sys
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This program trims an aligned sequence.")
	parser.add_argument("-ts", "--trim_start", dest="trim_start", type=str, nargs=1 , help="Trim n bases from the begining of the sequence.", required=True)
	parser.add_argument("-te", "--trim_end", dest="trim_end", type=str, nargs=1 , help="Trim n bases from the end of the sequence.", required=True)
	parser.add_argument("-in", "--input_fasta", dest="input_fasta", type=str, nargs=1 , help="Input alignment file.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the trimmed output file.", required=True) 
	args = parser.parse_args()
	return args

def map_contigs(file):
	contigs = {}
	for line in open(file, 'r'):
		if (">" in line):
			header = line
			sequence = ''
		elif (">" not in line):
			seq = line.strip("\n")
			sequence += seq
		contigs[header] = sequence
	return contigs

def main():

	myargs = create_parser()
	trim_start = myargs.trim_start[0]
	trim_trailing = myargs.trim_end[0]
	fasta_file = myargs.input_fasta[0]
	outfile = myargs.output_file[0]

	contigs = map_contigs(fasta_file)

	output = open(outfile, 'w')
	for header in contigs.keys():
		trim_end = len(contigs[header]) - int(trim_trailing)
		output.write(header)
		trimmed_seq = contigs[header][int(trim_start):int(trim_end)]
		for n in xrange(0,len(trimmed_seq), 80):
			output.write(str(trimmed_seq[n:n+80])+"\n")

	output.close()

if __name__ == '__main__':
	main()