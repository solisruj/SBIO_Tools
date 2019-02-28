#!/usr/bin/python

import pandas as pd 
import sys

input_file = sys.argv[1]
input_map = sys.argv[2]
output_file = sys.argv[3]

dataframe = pd.read_table(input_file, sep='\t', header=None)
map_file = pd.read_table(input_map, sep="\t", header=None)

map_dict = {}
for r in range(len(map_file)):
	map_dict[map_file.iloc[r:r+1,0].values[0]] = map_file.iloc[r:r+1,1].values[0]

for r in range(len(dataframe)):
	for c in range(len(dataframe.columns.values)):
		if ( dataframe.iloc[r:r+1,c].values[0] in map_dict.keys()):
			dataframe.iloc[r:r+1,c].values[0] = map_dict[dataframe.iloc[r:r+1,c].values[0]]

dataframe.to_csv(output_file, index=False, sep='\t', header=None)
