#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This outputs a dendogram for a given tab deliminated file.")
	parser.add_argument("-type", dest="plot_type", type=str, nargs=1, help="Plot type: default, standardize, normalize, correlation, euclidean, single, ward.", required=True) 
	parser.add_argument("-in", dest="input_file", type=str, nargs=1 , help="Input should be a two column tab deliminated file with column headers.", required=True)
	#parser.add_argument("-title", dest="title", type=str, nargs=1, help="Name of the graph: \"The graph\"", required=True) 
	parser.add_argument("-out", dest="output_file", type=str, nargs=1, help="Name of the output image file.", required=True) 
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	input_file = myargs.input_file[0]
	plot_type = myargs.plot_type[0]
	#title = myargs.title[0]
	output = myargs.output_file[0]

	dataframe = pd.read_table(input_file)

	count = 0
	for i in dataframe.iloc[2:3].values[0]:
		count += 1
		if ( isinstance(i, str)):
			break

	model_factor = dataframe.iloc[:,count-1:count].columns.values[0]
	dataframe = dataframe.set_index(model_factor)
	del dataframe.index.name
 
	if(plot_type == 'default'):
		dendogram = sns.clustermap(dataframe, cmap="mako")
	elif (plot_type == 'standardize'):
		dendogram = sns.clustermap(dataframe, robust=False, standard_scale=1, cmap="mako")
	elif (plot_type == 'normalize'):
		dendogram = sns.clustermap(dataframe, robust=False, z_score=1, cmap="mako")
	elif (plot_type == 'correlation'):
		dendogram = sns.clustermap(dataframe, robust=False, metric="correlation", standard_scale=1, cmap="mako")
	elif (plot_type == 'euclidean'):
		dendogram = sns.clustermap(dataframe, robust=False, metric="euclidean", standard_scale=1, cmap="mako")
	elif (plot_type == 'single'):
		dendogram = sns.clustermap(dataframe, robust=False, metric="euclidean", standard_scale=1, method="single", cmap="mako")
	elif (plot_type == 'ward'):
		dendogram = sns.clustermap(dataframe, robust=False, metric="euclidean", standard_scale=1, method="ward", cmap="mako")

	#dendogram.set_title(title)
	dendogram.savefig(output)

if __name__ == '__main__':
	main()