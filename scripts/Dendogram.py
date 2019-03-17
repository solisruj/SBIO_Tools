#!/usr/bin/env python

import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
import numpy as np
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This program outputs a dendogram from a given tab deliminated file.")
	parser.add_argument("-in", dest="input_file", type=str, nargs=1, help="Input is a tab delimated file with column headers.", required=True)
	#parser.add_argument("-title", dest="title", type=str, nargs=1, help="Title of the denodogram plot.", required=True)
	parser.add_argument("-out", dest="output", type=str, nargs=1, help="Name of the output png file.", required=True)
	args = parser.parse_args()
	return args

def main():
	myargs = create_parser()
	input_file = myargs.input_file[0]
	#plot_title = myargs.title[0]
	output = myargs.output[0]

	dataframe = pd.read_table(input_file) 

	count = 0
	for i in dataframe.iloc[2:3].values[0]:
		count += 1
		if (isinstance(i, str)):
			break

	model_factor = dataframe.iloc[:,count-1:count].columns.values[0]
	dataframe = dataframe.set_index(model_factor)
	del dataframe.index.name

	Z = hierarchy.linkage(dataframe, 'ward')

	dendogram = hierarchy.dendrogram(Z, orientation="left", labels=dataframe.index)
	#hierarchy.dendrogram(Z, orientation="left", labels=df.index)

	#Z.set_title(plot_title)
	#plt.show(dendogram)
	plt.tight_layout()
	plt.savefig(output)
	#figure = dendogram.get_figure()
	#figure.set_size_inches(8,7.5)
	#figure.savefig(out_file)

if __name__ == '__main__':
	main()