#!/usr/bin/env python3 
import os
import sys
import subprocess
import argparse
import pandas as pd

def create_parser():
	parser = argparse.ArgumentParser(description="This program returns Average Amino Identity Coverage, Score, and Similarity for mutltiple references.")
	parser.add_argument("-q", dest="query", type=str, nargs=1 , help="Input nucleotide sequence file (.faa).", required=True)
	parser.add_argument("-r", dest="reference", type=str, nargs=1, help="Reference directory containing reference files (.faa).", required=True) 
	args = parser.parse_args()
	return args

def main():

	myargs = create_parser()
	query = myargs.query[0]
	ref = os.path.abspath(myargs.reference[0])

	header = ['query']
	coverage = [query]
	score = [query]
	similarity = [query]
	
	for reference in os.listdir(ref):
		if(reference.endswith('.faa')):

			header.append(reference)
			ani_cmnd = ['Average_Amino_Identity.py', '-q', query, '-r', ref + '/' + reference]
			ani_out = subprocess.check_output(ani_cmnd)


			#print ani_out.split('\n')


			ani_content = ani_out.split('\n')[-3].split("\t")

			coverage.append(ani_content[-3])
			score.append(ani_content[-2])
			similarity.append(ani_content[-1])

	cov_df = pd.DataFrame([coverage])
	cov_df.columns = header
	sco_df = pd.DataFrame([score])
	sco_df.columns = header
	sim_df = pd.DataFrame([similarity])
	sim_df.columns = header

	cov_df.to_csv(query.split('.')[0]+'_coverage.tsv', index=False, sep="\t")
	sco_df.to_csv(query.split('.')[0]+'_score.tsv', index=False, sep="\t")
	sim_df.to_csv(query.split('.')[0]+'_similarity.tsv', index=False, sep="\t")


if __name__ == '__main__':
	main()