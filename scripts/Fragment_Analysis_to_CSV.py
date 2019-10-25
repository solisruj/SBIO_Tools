#!/usr/bin/env python3

import argparse
import pandas as pd
from Bio import SeqIO
from collections import defaultdict
import matplotlib.pyplot as plt

def create_parser():
	parser = argparse.ArgumentParser(description="This program takes in FSA/ABI files and converts them to CSV files.")
	parser.add_argument("-i", dest="input", type=str, nargs=1 , help="Input FSA/ABI", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Output CSV name", required=False, default=True)
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	infile = myargs.input[0]

	if myargs.output:
		if infile.endswith('.fsa'):
	 		outfile = infile.split('.fsa')[0] + '.csv'
		elif infile.endswith('.abi'):
	 		outfile = infile.split('.abi')[0] + '.csv'

	record = SeqIO.read(infile, 'abi')
	channels = ['DATA1', 'DATA2', 'DATA3', 'DATA4']
	trace = defaultdict(list)
	for c in channels:
		trace[c] = record.annotations['abif_raw'][c]

	trace_df = pd.DataFrame.from_dict(trace, orient='index').reset_index().transpose()
	#trace_df.columns = ['Channel_1', 'Channel_2', 'Channel_3', 'Channel_4']
	
	trace_df.to_csv(outfile, sep=',', header=False, index=False)



if __name__ == '__main__':
	main()


