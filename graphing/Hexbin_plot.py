#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a hexbin plot for a a given tab deliminated data text file.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be a two column tab deliminated file with column headers. The first column should be x-axis, y-axis should be values.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output image file.", required=True) 
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	input_file = myargs.input_file[0]
	output_file = myargs.output_file[0]

	dataframe = pd.read_table(input_file, sep='\t')
	factors = dataframe.columns.tolist()

	with sns.axes_style("white"):
		hexbin = sns.jointplot(x=dataframe[factors[0]], y=dataframe[factors[1]], kind="hex", color="k")

	hexbin.savefig(output_file)

if __name__ == "__main__":
	main()

