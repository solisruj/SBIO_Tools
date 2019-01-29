#!/usr/bin/python

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a scatterplot for a a given csv file containing a two quantitative columns, and one catagorical column data type.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be a multiple column csv file.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output image scatterplot matrix file.", required=True) 
	args = parser.parse_args()
	return args

def main():
	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	out_file = myargs.output_file[0]

	dataframe = pd.read_table(input_file, sep=",")
	sns.set(style="ticks")

	count = 0
	for i in dataframe.iloc[2:3].values[0]:
		count += 1
		if ( isinstance(i, str)):
			break

	sns.set(style="darkgrid")
	hue_factor = dataframe.iloc[:,count-1:count].columns.values[0]
	scatter_plot = sns.relplot(x=dataframe.columns.values[0], y=dataframe.columns.values[1], hue=hue_factor, data=dataframe);
	scatter_plot.savefig(out_file)

if __name__ == '__main__':
	main()