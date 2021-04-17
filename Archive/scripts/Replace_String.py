#!/usr/bin/env python3

import argparse
import pandas as pd 
import sys
import os

def create_parser():
	parser = argparse.ArgumentParser(description="This program replaces column names, and first column row name.")
	parser.add_argument("-in", dest="input_file", type=str, nargs=1 , help="Input file.", required=True)
	parser.add_argument("-mp", dest="map_file", type=str, nargs=1 , help="Map file.", required=True)
	parser.add_argument("-out", dest="output_file", type=str, nargs=1, help="Name of the output filename.", required=True) 
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	input_file = os.path.abspath(myargs.input_file[0])
	input_map = os.path.abspath(myargs.input_map[0])
	output_file = os.path.abspath(myargs.output_file[0])

	dataframe = pd.read_table(input_file, sep='\t', header=None)
	map_file = pd.read_table(input_map, sep="\t", header=None)

	map_dict = {}
	for r in range(len(map_file)):
		map_dict[map_file.iloc[r:r+1,0].values[0]] = map_file.iloc[r:r+1,1].values[0]

	for r in range(len(dataframe)):
		for c in range(len(dataframe.columns.values)):
			if ( dataframe.iloc[r:r+1,c].values[0] in map_dict.keys()):
				dataframe.iloc[r:r+1,c].values[0] = map_dict[dataframe.iloc[r:r+1,c].values[0]]

	dataframe.to_csv(output_file, index=False, sep='\t', header=None)

if __name__ == '__main__':
	main()
