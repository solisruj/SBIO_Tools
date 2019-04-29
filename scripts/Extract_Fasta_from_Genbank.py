#!/usr/bin/env python3

import argparse
import sys, os
from Bio import GenBank, SeqIO


def create_parser():
	parser = argparse.ArgumentParser(description="This program extracts fasta sequence form genbank file and outputs .fna file.")
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input fasta file.", required=True)
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	gbk_filename = myargs.input[0]

	#gbk_filename = "./GCA_000009065.1_ASM906v1_genomic.gbff"

	root_name = os.path.splitext(gbk_filename)[0]
	faa_filename = root_name + "_converted.fna"

	input_handle  = open(gbk_filename, "r")
	output_handle = open(faa_filename, "w")

	for seq_record in SeqIO.parse(input_handle, "genbank") :
		print ("Dealing with GenBank record %s" % seq_record.id)
		#print ">" + seq_record.id + "|" + seq_record.description
		#print seq_record.seq
		output_handle.write(">" + seq_record.id + "|" + seq_record.description + '\n')
		for n in range(0,len(seq_record.seq), 70):
			output_handle.write(str(seq_record.seq[n:n+70])+"\n")

	output_handle.close()
	input_handle.close()
	print ("Done")

if __name__ == '__main__':
	main()