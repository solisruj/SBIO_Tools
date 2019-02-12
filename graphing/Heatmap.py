#!/usr/bin/python

import seaborn as sns
import pandas as pd
import argparse

# Creating TUI parser for users.
def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a heatmap for a given tab deliminated matrix file.")
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1 , help="Input should be tab deliminated matrix with corresponding labels for columns and rows.", required=True)
	parser.add_argument("-title", "--title", dest="title", type=str, nargs=1, help="Name of the graph: \"The graph\"", required=True) 
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output image file.", required=True) 
	args = parser.parse_args()
	return args

def main():

	# Importing command-line arguments.
	myargs = create_parser()
	input_file = myargs.input_file[0]
	title = myargs.title[0]
	out_file = myargs.output_file[0]

	sns.set(style='whitegrid')

	df = pd.read_table(input_file, sep='\t', index_col=0)
	heatmap = sns.heatmap(df, cmap='YlGnBu', annot=True, annot_kws={'size':6})

	heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation = 0, fontsize = 6)
	heatmap.set_xticklabels(heatmap.get_yticklabels(), rotation = 90, fontsize = 6)
	heatmap.set_title(title)

	figure = heatmap.get_figure()
	figure.savefig(out_file, bbox_inches = 'tight')

if __name__ == '__main__':
	main()









