#!/usr/bin/env python3

import pandas as pd
import argparse
import subprocess as sub
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program gets variant annotations from OncoKB using their REST API.")
	parser.add_argument("-i", dest="input", type=str, nargs=1 , help="Input CSV/TSV file containing hgvsg's (No Column Headers): 15:g.90631934C>T", required=True)
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

def get_oncokb(hgvsg):
	chrom = hgvsg.split(':')[0]
	gdot = hgvsg.split(':')[1].split('>')[0]
	alt = hgvsg.split(':')[1].split('>')[1]
	https = 'https://oncokb.org:443/api/v1/annotate/mutations/byHGVSg?hgvsg=' + chrom + '%3A' + gdot + '%3E' + alt + '%09'
	#print(https)
	hgvsg_req = ['curl', '-X', 'GET', '--header', "'Accept: application/json'", https]
	try:
		print('Downloading:', hgvsg)
		hgvsg = hgvsg.replace(':', '.')
		hgvsg = hgvsg.replace('>', '.')
		annotations = open(hgvsg+'.json', "w")
		sub.call(hgvsg_req, stdout=annotations)
	except:
		print('ERROR:', hgvsg_req, 'Possibly Not Found')

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
