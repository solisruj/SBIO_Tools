#!/usr/bin/python

# A quick program to create barplots with pythons seaborns module. 
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Creating TUI parser for users.
def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a barplot for a a given tab deliminated data text file.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be a two column tab deliminated file with column headers. The first column should be x-axis, y-axis should be values.", required=True)
	parser.add_argument("-title", "--title", dest="title", type=str, nargs=1, help="Name of the graph: \"The graph\"", required=True) 
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output image file.", required=True) 
	args = parser.parse_args()
	return args

# Main body of the program.
def main():
	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	title = myargs.title[0]
	out_file = myargs.output_file[0]

	# Loading the dataframe, factor names, and labels. 
	dataframe = pd.read_table(input_file, sep="\t")
	factors = dataframe.columns.tolist()
	labels = dataframe[factors[0]].tolist()

	# Setting the seaborns style to whitegrid, and formatting the graph. 
	sns.set(style='whitegrid')
	barplot = sns.barplot(x=dataframe.index, y=dataframe[factors[1]], data=dataframe)
	barplot.set(xlabel=factors[0], ylabel=factors[1])
	barplot.set_xticklabels(labels, rotation='vertical', fontsize=8)
	barplot.set_title(title)

	# Getting the figure, and setting the figure size to correctly fit within the image, and then saving to a file. 
	figure = barplot.get_figure()
	figure.set_size_inches(10.5,13)
	figure.savefig(out_file)

if __name__ == '__main__':
	main()