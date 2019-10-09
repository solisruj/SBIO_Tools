#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program takes in a CSV file and adds gnomAD annotations: Allele Counts, Total Allele Number, Allele Frequency, and Allele Type.")
	parser.add_argument("-db", dest="db", type=str, nargs=1 , help="gnomAD database .vcf file. File extension must be changed to .gz, and then decompressed with gunzip.", required=True)
	parser.add_argument("-in", dest="input", type=str, nargs=1 , help="Input CSV containing the following columns (label headers as such): MRN, LabID, Chromosome, Position_start, Reference, Variant", required=True)
	parser.add_argument("-out", dest="output", type=str, nargs=1, help="Path to the output directory.", required=True)
	parser.add_argument("-name", dest="name", type=str, nargs=1, help="Output file name.", required=True) 
	args = parser.parse_args()
	return args

def to_dataframe(file):
	if file.endswith('.csv'):
		df = pd.read_csv(file, sep=',')
	elif file.endswith('.tsv'):
		df = pd.read_csv(file, sep='\t')
	else:
		raise ValueError('ERROR: Input file is not .csv or .tsv')
	return df

def dataframe_to_dict(dataframe):
	variants = {}
	vh = []
	for col_name in dataframe.columns.tolist():
		if 'chr' in col_name.lower():
			vh.append(col_name)
		elif 'start' in col_name.lower():
			vh.append(col_name)
		elif 'ref' in col_name.lower():
			vh.append(col_name)
		elif 'alt' in col_name.lower():
			vh.append(col_name)

	col_names = dataframe.columns.tolist()
	for i in range(len(dataframe)):
		chrom = str(dataframe.iloc[i:i+1, col_names.index(vh[0])].values[0])
		start = str(dataframe.iloc[i:i+1, col_names.index(vh[1])].values[0])
		ref = str(dataframe.iloc[i:i+1, col_names.index(vh[2])].values[0])
		alt = str(dataframe.iloc[i:i+1, col_names.index(vh[3])].values[0])

		identifier = '-'.join([chrom, start, ref, alt ])
		variants[identifier] = True

	return variants, vh

def read_vcf(database, variants):
	for line in open(database, 'r'):
		if '#' not in line:
			lp = line.split('\t')
			identifier = '-'.join([lp[0], lp[1], lp[3], lp[4]])
			if identifier in variants.keys():
				lp_sub = lp[7].split(';')
				if 'AC' in lp_sub[0] and 'AN' in lp_sub[1]:
					ac = lp_sub[0].split('=')[1]
					an = lp_sub[1].split('=')[1]
					af = float(lp_sub[0].split('=')[1]) / float(lp_sub[1].split('=')[1])
					print("Found:", identifier) #, ac, an, af)
					variants[identifier] = [ac, an, af]
	return variants

def annotate_df(dataframe, cnames, variants):
	col_name = dataframe.columns.tolist()

	if col_name[-1] == 'gnomeAD.alt_allele_Freq':
		for i in range(len(dataframe)):
			chrom = str(dataframe.iloc[i:i+1, col_name.index(cnames[0])].values[0])
			start = str(dataframe.iloc[i:i+1, col_name.index(cnames[1])].values[0])
			ref = str(dataframe.iloc[i:i+1, col_name.index(cnames[2])].values[0])
			alt = str(dataframe.iloc[i:i+1, col_name.index(cnames[3])].values[0])
			identifier = '-'.join([chrom, start, ref, alt ])

			if variants[identifier] != True:
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.alt_allele_count')].values[0] = float(variants[identifier][0])
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.total_number_of_alleles')].values[0] = float(variants[identifier][1])
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.alt_allele_Freq')].values[0] = float(variants[identifier][2])
	else:
		dataframe['gnomeAD.alt_allele_count'] = None
		dataframe['gnomeAD.total_number_of_alleles'] = None
		dataframe['gnomeAD.alt_allele_Freq'] = None

		col_name = dataframe.columns.tolist()
		for i in range(len(dataframe)):
			chrom = str(dataframe.iloc[i:i+1, col_name.index(cnames[0])].values[0])
			start = str(dataframe.iloc[i:i+1, col_name.index(cnames[1])].values[0])
			ref = str(dataframe.iloc[i:i+1, col_name.index(cnames[2])].values[0])
			alt = str(dataframe.iloc[i:i+1, col_name.index(cnames[3])].values[0])
			identifier = '-'.join([chrom, start, ref, alt ])

			if variants[identifier] != True:
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.alt_allele_count')].values[0] = float(variants[identifier][0])
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.total_number_of_alleles')].values[0] = float(variants[identifier][1])
				dataframe.iloc[i:i+1, col_name.index('gnomeAD.alt_allele_Freq')].values[0] = float(variants[identifier][2])
	return dataframe

def main():

	myargs = create_parser()
	database = myargs.db[0]
	infile = myargs.input[0]
	outpath = myargs.output[0]
	name = myargs.name[0]

	database = os.path.abspath(database)
	infile = os.path.abspath(infile)
	outpath= os.path.abspath(outpath)

	df = to_dataframe(infile)
	var_dict, col_name = dataframe_to_dict(df)
	var_dict = read_vcf(database, var_dict)

	anote_df = annotate_df(df, col_name,var_dict)
	anote_df.to_csv(outpath+'/'+name, sep=',', index=False)

if __name__ == '__main__':
	main()