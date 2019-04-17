#!/usr/bin/python

# Importing modules.
import pandas as pd
import sys
import argparse

# Funciton to take in command-line arguments.
def create_parser():
	parser = argparse.ArgumentParser(description="This program sorts Average Nucleotide Identity (ANI) coverage and score of the subject to the refence and lists them in decsending order.")
	parser.add_argument("-mp", "--map_file", dest="map_file", type=str, nargs=1 , help="Input map file. This is a tab deliminated file of bacterial accession IDs and Bacterial Names.", required=True)
	parser.add_argument("-c", "--coverage_file", dest="coverage_file", type=str, nargs=1, help="ANI coverage file.", required=True)
	parser.add_argument("-s", "--score_file", dest="score_file", type=str, nargs=1, help="ANI score file.", required=True)
	parser.add_argument("-o", "--out_file", dest="out_file", type=str, nargs=1, help="Name of the output file.", required=True) 
	args = parser.parse_args()
	return args

# Funciton to convert the map file into a dictionary for quick access. 
def map_file(lst):
        map_dict = {}
        for r in range(len(lst)):
                map_dict[lst.iloc[r:r+1,1].values[0]] = lst.iloc[r:r+1,0].values[0]
        return map_dict

# This function converts finds the strain IDS/Accessions and replaces them with the bacterial name. 
def strain_to_taxonomy(df, mp_dct):
	for key in mp_dct:
		for c in range(len(df.columns)):
			if(key in str(df.iloc[0:1,c].values[0])):
				df.iloc[0:1,c].values[0] = mp_dct[key]
		for r in range(len(df)):
			if(key in str(df.iloc[r:r+1,0].values[0])):
				df.iloc[r:r+1,0].values[0] = key
	return df

# This function sorts the coverage and the score of the reference in descending order of coverage and then score to the subject strain.
def sort_frame(df_cov, df_score, outFile):
	with open(outFile, 'w') as out_file:
		for r in range(1,len(df_cov)):
			cov_dict = {}
			scor_dict = {}
			acsn = str(df_cov.iloc[r:r+1,0].values[0]+"\tCoverage\tScore\n")
			out_file.write(acsn)
			for c in range(1,len(df_cov.columns)):
				cov_dict[df_cov.iloc[0:1,c].values[0]] = df_cov.iloc[r:r+1,c].values[0]
				scor_dict[df_score.iloc[0:1,c].values[0]] = df_score.iloc[r:r+1,c].values[0]
			sorted_dict = sorted(cov_dict, key=lambda x: cov_dict[x], reverse=True)
			for key in sorted_dict:
				line = str("{}\t{}".format(key, cov_dict[key])+"\t"+scor_dict[key]+"\n")
				out_file.write(line)
			out_file.write("\n")

# Main body of the program.
def main():
	myargs = create_parser()
	file_map = myargs.map_file[0]
	file_cov = myargs.coverage_file[0]
	file_scor = myargs.score_file[0]
	file_out = myargs.out_file[0]
	#print file_map, file_cov, file_scor, file_out
	mpfle = pd.read_table(file_map, header=None)
	coverage = pd.read_table(file_cov, header=None, sep="\t")
	score = pd.read_table(file_scor, header=None, sep="\t")
	mapped = map_file(mpfle)
	cov = strain_to_taxonomy(coverage, mapped)
	scor = strain_to_taxonomy(score, mapped)
	sort_frame(cov, scor, file_out )
	
if __name__ == '__main__':
	main()