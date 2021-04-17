#!/usr/bin/env python3

import argparse
import sys, os
from Bio import GenBank, SeqIO

def create_parser():
	parser = argparse.ArgumentParser(description="This program extracts coding sequences (CDS) form genbank file and outputs .faa file.")
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input fasta file.", required=True)
	args = parser.parse_args()
	return args

def main():
	
	myargs = create_parser()
	gbk_filename = myargs.input[0]
	#gbk_filename = './GCA_000009065.1_ASM906v1_genomic.gbff'

	root_name = os.path.splitext(gbk_filename)[0]
	faa_filename = root_name + "_converted.faa"

	input_handle  = open(gbk_filename, "r")
	output_handle = open(faa_filename, "w")

	for seq_record in SeqIO.parse(input_handle, "genbank") :
		print ("Dealing with GenBank record %s" % seq_record.id)
		for seq_feature in seq_record.features :
			if seq_feature.type=="CDS" :
				if ('locus_tag' in seq_feature.qualifiers and 'translation' in seq_feature.qualifiers):
					assert (len(seq_feature.qualifiers['translation'])==1)
					output_handle.write(">%s from %s\n%s\n" % (seq_feature.qualifiers['locus_tag'][0], seq_record.name, seq_feature.qualifiers['translation'][0]))
				if ('protein_id' in seq_feature.qualifiers and 'translation' in seq_feature.qualifiers and 'locus_tag' not in seq_feature.qualifiers):
					assert (len(seq_feature.qualifiers['translation'])==1)
					output_handle.write(">%s from %s\n%s\n" % (seq_feature.qualifiers['protein_id'][0], seq_record.name, seq_feature.qualifiers['translation'][0]))

	output_handle.close()
	input_handle.close()
	print ("Done")

if __name__ == '__main__':
	main()