#!/usr/bin/python

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a histogram for a a given csv file containing one quantitative data column.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be a single column csv file.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output histogram png file.", required=True) 
	args = parser.parse_args()
	return args

def main():
	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	out_file = myargs.output_file[0]

	dataframe = pd.read_table(input_file, sep=",")

	dataframe = pd.read_table('./Single_Values.csv', sep=",")

	factors = dataframe.columns.tolist()
	histogram = sns.distplot(dataframe)

	histogram.set_ylabel('Frequency')
	histogram.set_xlabel(factors[0])
	#histogram.savefig(out_file)

	figure = histogram.get_figure()
	figure.set_size_inches(8,7.5)
	figure.savefig(out_file)


if __name__ == '__main__':
	main()


