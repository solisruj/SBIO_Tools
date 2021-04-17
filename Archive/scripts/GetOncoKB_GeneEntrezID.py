#!/usr/bin/env python3

import pandas as pd
import argparse
import subprocess as sub
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program gets gene information from OncoKB using their REST API.")
	parser.add_argument("-i", dest="input", type=str, nargs=1 , help="Input CSV/TSV file containing gene names (No Column Headers).", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Path to the output directory.", required=True) 
	args = parser.parse_args()
	return args

def read_file(input_file):
	if input_file.endswith('.csv'):
		df = pd.read_csv(input_file, sep=',', header=None)
		return df
	elif input_file.endswith('.tsv'):
		df = pd.read_csv(input_file, sep='\t', header=None)
		return df
	else:
		raise ValueError('Error: Input file is not .csv or .tsv')

def get_oncokb(gene):
	https = 'https://oncokb.org:443/api/v1/genes/lookup?query=' + gene
	#print(https)
	gene_req = ['curl', '-X', 'GET', '--header', "'Accept: application/json'", https]
	try:
		print('Downloading:', gene)
		annotations = open(gene+'.json', "w")
		sub.call(gene_req, stdout=annotations)
	except:
		print('ERROR:', gene, 'Possibly Not Found')

def main():

	myargs = create_parser()
	input_file = myargs.input[0]
	output_dir = myargs.output[0]

	abs_input_file = os.path.abspath(input_file)
	abs_output_dir = os.path.abspath(output_dir)
	os.chdir(abs_output_dir)

	hgvsg_df = read_file(abs_input_file)

	for index, row in hgvsg_df.iterrows():
		get_oncokb(row[0])
		
if __name__ == '__main__':
	main()
