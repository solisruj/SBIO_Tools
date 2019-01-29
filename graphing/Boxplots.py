#!/usr/bin/python

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Creating a simple TUI parser to take command line arguments. 
def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a boxplot for a a given csv file containing one quantitative column and one catagorical column.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be a two column csv file.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output boxplot png file.", required=True) 
	args = parser.parse_args()
	return args

def main():
	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	out_file = myargs.output_file[0]

	# Importing data into a pandas dataframe and passing factors to a variable.
	dataframe = pd.read_table(input_file, sep=",")
	factors = dataframe.columns.tolist()

	# Setting the boxplot from sns.catplot and saving the figure.
	boxplot = sns.catplot(x=factors[1], y=factors[0], kind="box", data=dataframe)
	boxplot.savefig(out_file)

if __name__ == '__main__':
	main()
