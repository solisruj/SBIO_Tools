#!/usr/bin/python

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Creating the a user friendly commandlin based TUI.
def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a scatterplot matrix for a a given csv file containing a catagorical data type.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should multiple column csv file.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output image scatterplot matrix file.", required=True) 
	args = parser.parse_args()
	return args

def main():
	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	out_file = myargs.output_file[0]

	# Setting the dataframe and setting the style of scatter plot matrix to ticks. 
	dataframe = pd.read_table(input_file, sep=",")
	sns.set(style="ticks")

	# Iterating throught the first list of values to determine which column is the catergorical column.
	count = 0
	for i in dataframe.iloc[2:3].values[0]:
		count += 1
		if ( isinstance(i, str)):
			break

	# Setting the hue factor and calling the pair plots. 
	hue_factor = dataframe.iloc[:,count-1:count].columns.values[0]
	pair_plot = sns.pairplot(dataframe, hue=hue_factor)

	# Saving the figure. 
	pair_plot.savefig(out_file)
	#figure = pair_plot.get_figure()
	#figure.set_size_inches(10.5,13)
	#figure.savefig(out_file)

if __name__ == '__main__':
	main()