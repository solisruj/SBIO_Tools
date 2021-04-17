#!/usr/bin/env python3

import pandas as pd
import argparse
import subprocess as sub
import json
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program takes in a CSV file containing MRN, LABID, CHROMOSOME, POSITION, REFERENCE, and VARIANT and annotates them with\
		variant population frequencies from a folder containing JSON files. These JSON files contain variant population freqncies. Please use the following program to download\
		JSONS: Get_ExAC_Variant_Annotations.py. Use -h for help.")
	parser.add_argument("-d", dest="dir", type=str, nargs=1 , help="Input directory containing all the variant JSON files.", required=True)
	parser.add_argument("-i", dest="input", type=str, nargs=1 , help="Input CSV containing the following columns (label headers as such): MRN, LabID, Chromosome, Position_start, Reference, Variant", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Path to the output directory.", required=True)
	parser.add_argument("-n", dest="name", type=str, nargs=1, help="Output file name.", required=True) 
	args = parser.parse_args()
	return args

def load_json(json_file):
	jfile = open(json_file)
	data = json.load(jfile)
	jfile.close()
	return data

def parse_jsons(json_directory):
	pacs = {}
	pans = {}
	anum = {}
	columns = []
	jsons = os.listdir(json_directory)
	for json in jsons:
		variant = json.split('.')[0]
		jpath = json_directory + '/' + json
		jdata = load_json(jpath)
		if 'pop_acs' in jdata.keys() and 'pop_ans' in jdata.keys() and 'allele_num' in jdata.keys():
			pacs[variant] = jdata['pop_acs']
			pans[variant] = jdata['pop_ans']
			anum[variant] = jdata['allele_num']
			for key in jdata['pop_acs']:
				columns.append(key)
		else:
			pacs[variant] = 'No Annnotations Available'
			pans[variant] = 'No Annnotations Available'
			anum[variant] = 'No Annnotations Available'
	return pacs, pans, anum, list(set(columns))

def read_file(input_file):
	if input_file.endswith('.csv'):
		df = pd.read_csv(input_file, sep=',')
	else:
		raise ValueError('ERROR: Input file is not .csv')
	return df

def annotate(dataframe, pop_acs, pop_ans, allele_num, columns, out_path):
	for col in columns:
		dataframe[col+' pop acs'] = None
		dataframe[col+' pop ans'] = None
		dataframe[col+' freq'] = None
	dataframe['Pop Frequncy'] = None

	col_names = dataframe.columns.tolist()
	for i in range(len(dataframe)):
		chrom = str(dataframe.iloc[i:i+1, col_names.index('Chromosome')].values[0])
		start = str(dataframe.iloc[i:i+1, col_names.index('Position_start')].values[0])
		ref = str(dataframe.iloc[i:i+1, col_names.index('Reference')].values[0])
		var = str(dataframe.iloc[i:i+1, col_names.index('Variant')].values[0])

		identifier = chrom + '-' + start + '-' + ref + '-' + var

		occurence = 0
		if identifier in pop_acs.keys():
			if pop_acs[identifier] != 'No Annnotations Available': 
				for key, value in pop_acs[identifier].items():
					#print(key, value, pop_ans[identifier][key])
					dataframe.iloc[i:i+1, col_names.index(key +' pop acs')].values[0] = value
					dataframe.iloc[i:i+1, col_names.index(key +' pop ans')].values[0] = pop_ans[identifier][key]
					if pop_ans[identifier][key] != 0:
						dataframe.iloc[i:i+1, col_names.index(key +' freq')].values[0] = float(value) / float(pop_ans[identifier][key]) 
					occurence += value

				dataframe.iloc[i:i+1, col_names.index('Pop Frequncy')].values[0] = float(occurence) / float(allele_num[identifier])

	return dataframe

def main():

	myargs = create_parser()
	indir = myargs.dir[0]
	input_file = myargs.input[0]
	out = myargs.output[0]
	name = myargs.name[0]

	dir_path = os.path.abspath(indir)
	file_path = os.path.abspath(input_file)
	out_path = os.path.abspath(out)

	df = read_file(file_path)
	pop_acs, pop_ans, allele_num, columns = parse_jsons(dir_path)

	annotated_df = annotate(df, pop_acs, pop_ans, allele_num, columns, out_path)
	annotated_df.to_csv(out_path + '/' + name)


if __name__ == '__main__':
	main()
