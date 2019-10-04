#!/usr/bin/env python3

import pandas as pd
import argparse
import subprocess as sub
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program uses ExAC's REST service to download variant JSON formatted files. It will retrieve individual JSON files for each specified\
		variant in a given input CSV file. ")
	parser.add_argument("-i", dest="input", type=str, nargs=1 , help="Input CSV file with the following columns (Do Not Include Column Headers): LAB_ID, CHROMOSOME, POSITION, REFERENCE, VARIANT", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Path to the output directory.", required=True) 
	args = parser.parse_args()
	return args

def get_exac(variant):
	var_req = ['wget', 'http://exac.hms.harvard.edu/rest/variant/variant/' + variant]
	try:
		sub.call(var_req)
	except:
		print('ERROR:', variant, 'Possibly Not Found')

def read_file(input_file):
	if input_file.endswith('.csv'):
		df = pd.read_csv(input_file, sep=',', header=None)
		return df
	else:
		raise ValueError('Error: Input file is not .csv or .txt')

def main():

	myargs = create_parser()
	input_file = myargs.input[0]
	output_dir = myargs.output[0]

	abs_input_file = os.path.abspath(input_file)
	abs_output_dir = os.path.abspath(output_dir)

	print(abs_input_file, abs_output_dir)
	os.chdir(abs_output_dir)

	variants_df = read_file(abs_input_file)

	for index, row in variants_df.iterrows():
		row = row.values.tolist()
		row = [str(x) for x in row[1:]]
		get_exac('-'.join(row))

if __name__ == '__main__':
	main()
