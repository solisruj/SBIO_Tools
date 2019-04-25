#!/usr/bin/python

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Creating a simple TUI interface for the command-line. 
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

	sns.set(color_codes=True)

	# Loading the dataframe. 
	dataframe = pd.read_csv(input_file, sep='\t')

	# Setting the column factors to a variable.
	factors = dataframe.columns.tolist()

	# Creating the histogram on the dataframe using sns.distplot, and adding an x/y label.
	histogram = sns.distplot(dataframe)
	histogram.set_ylabel('Frequency')
	histogram.set_xlabel(factors[0])
	#histogram.savefig(out_file)

	# Getting the figure from and setting the figure size. Then saving the histogram. 
	figure = histogram.get_figure()
	figure.set_size_inches(8,7.5)
	figure.savefig(out_file, dpi=300, bbox_inches = 'tight')

if __name__ == '__main__':
	main()


