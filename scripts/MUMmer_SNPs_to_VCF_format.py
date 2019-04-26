#!/usr/bin/env python3

import argparse
import os
import math

def create_parser():
	parser = argparse.ArgumentParser(description="This program coverts a MUMer SNP file to VCF format.")
	parser.add_argument("-q", dest="bsa", type=float, nargs=1 , default=99.9, help="Base call accuracy is set to: Default: 99.9 (quality of 30). For increase quality increase 99.9 to 99.99, 99.999, etc.. ", required=False)
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input MUMer snps file.", required=True)
	parser.add_argument("-out", dest="output", type=str, nargs=1, help="Name of the VCF output file.", required=True) 
	args = parser.parse_args()
	return args


def calc_phred_quality(accuracy):
	phred_quality = (-10) * math.log10((1 - (accuracy / 100.00)))
	return phred_quality

def parse_snps(snps_file, accuracy, out):
	for line in open(snps_file, 'r'):
		if ('/' not in line and '[' not in line and 'NUCMER' not in line and len(line.split('\t')) > 1):
			snps_lines = line.strip('\n').split('\t')
			#print(snps_lines[2])
			if (accuracy != 99.9):
				Q = calc_phred_quality(accuracy[0])
				snp_info = [snps_lines[13], snps_lines[0], '.', snps_lines[1], snps_lines[2], str(round(Q,2 )), 'PASS', '.', 'GT', '1/1']
				out.write('\t'.join(snp_info)+'\n')
			elif (accuracy == 99.9):
				snp_info = [snps_lines[13], snps_lines[0], '.', snps_lines[1], snps_lines[2], '30', 'PASS', '.', 'GT', '1/1']
				out.write('\t'.join(snp_info)+'\n')

def main():

	myargs = create_parser()
	base_call_accuracy = myargs.bsa
	mum_snps_file = os.path.abspath(myargs.input[0])
	output = os.path.abspath(myargs.output[0])

	vcf_version = '##fileformat=VCFv4.2\n'
	vcf_format = '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
	vcf_header = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL' , 'FILTER', 'INFO', 'FORMAT', 'sample1']

	output_file = open(output, 'w')
	output_file.write(vcf_version)
	output_file.write(vcf_format)
	output_file.write('\t'.join(vcf_header)+'\n')
	parse_snps(mum_snps_file, base_call_accuracy, output_file )

	output_file.close()


if __name__ == '__main__':
	main()