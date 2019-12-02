#!/usr/bin/env python3

import pandas as pd
import numpy as np
import argparse
import subprocess as sub
import os
import sys
import json
import shutil

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program takes in a directory containing OncoKB gene information and parses Entrez Gene ID.")
	parser.add_argument("-d", dest="input", type=str, nargs=1 , help="Input directory.", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Path to the output CSV.", required=True) 
	args = parser.parse_args()
	return args

def rename_file(file):
	parts = file.split(', ')
	new_filename = '_'.join(parts)
	shutil.move(file, new_filename)
	return new_filename


def load_json(json_file):
	with open(json_file, 'r') as j:
		contents = json.loads(j.read())
	return contents

def parse_jsons(files):
	genes = {}
	for file in files:

		if ' ' in file:
			file = rename_file(file)

		if os.stat(file).st_size != 0:

			gene = file.split('.')[0].split('/')[-1]

			if '_' in gene:
				gene = ', '.join(gene.split('_'))
			GeneInfo = load_json(file)

			if len(GeneInfo) != 0:
				genes[gene] = GeneInfo[0]['entrezGeneId']

		else:
			gene = file.split('.')[0].split('/')[-1]
			if '_' in gene:
				gene = ', '.join(gene.split('_'))
			genes[gene] = np.nan

			if 'LOC' in gene:

				ID = gene.split('LOC')[1]
				if ' ' in ID:
					ID = ID.split(',')[0]

				genes[gene] = ID

	return genes

def main():

	myargs = create_parser()
	input_dir = myargs.input[0]
	output_dir = myargs.output[0]

	inpath = os.path.abspath(input_dir)
	outpath = os.path.abspath(output_dir)

	files = os.listdir(inpath)
	files = [inpath+'/'+file for file in files]
	
	genes = parse_jsons(files)

	df = pd.DataFrame(list(genes.items()))
	df.columns = ['Gene', 'Entrez ID']
	df.to_csv(outpath+'/gene_entrez.id.csv', index=False)

if __name__ == '__main__':
	main()