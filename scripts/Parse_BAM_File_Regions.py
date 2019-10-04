#!/usr/bin/env python3

import pandas as pd
import argparse
import subprocess as sub
import os
import sys

# Command-line argument parser.
def create_parser():
	parser = argparse.ArgumentParser(description="This program parses out BAM file regions of interest and returns a generated BAM file containing only the Region Of Interet. It takes in a CSV \
		containing the following columns: MRN, LabID, Chromosome, Position_Start, Position_End. It also requires a local \
		installation of Samtools >= 1.9 and htslib >= 1.9")
	parser.add_argument("-i", "--input", dest="input", type=str, nargs=1 , help="Input CSV file.", required=True)
	parser.add_argument("-b", "--bam", dest="bam", type=str, nargs=1 , help="Input bam file.", required=True)
	#parser.add_argument("-o", "--output", dest="output", type=str, nargs=1, help="Name of the output bam file.", required=True) 
	args = parser.parse_args()
	return args

def file_to_dataframge(input_file):
	if input_file.endswith('.csv'):
		df = pd.read_csv(input_file, sep=',')
		return df

def map_variants(dataframe):

	col_names = dataframe.columns.tolist()
	cname_dict = {}
	labid_dict = {}

	for cname in col_names:

		if 'mrn' in cname.lower():
			cname_dict[cname] = 'MRN'
		elif 'b_id' in cname.lower():
			cname_dict[cname] = 'LabID'
		elif 'chr' in cname.lower():
			cname_dict[cname] = 'Chromosome'
		elif 'start' in cname.lower():
			cname_dict[cname] = 'Pos_Start'
		elif 'end' in cname.lower():
			cname_dict[cname] = 'Pos_End'

	dataframe = dataframe.rename(columns=cname_dict)

	col_names = dataframe.columns.tolist()
	#print(col_names)
	for i in range(len(dataframe)):
		#mrn = float(dataframe.iloc[i:i+1, col_names.index('MRN')].values[0])
		labid = str(dataframe.iloc[i:i+1, col_names.index('LabID')].values[0])
		chrom = str(dataframe.iloc[i:i+1, col_names.index('Chromosome')].values[0])
		start = float(dataframe.iloc[i:i+1, col_names.index('Pos_Start')].values[0])
		end = float(dataframe.iloc[i:i+1, col_names.index('Pos_End')].values[0])

		if labid in labid_dict.keys():
			labid_dict[labid].append([ chrom, start, end])
		else:
			labid_dict[labid] = [[ chrom, start, end]]

	return labid_dict

def start_position(value):
	value = round(value)
	val = str(value)[:4] + (len(str(int(value))) - 4) * '0'
	return val

def end_position(value):
	value = round(value)
	val = str(int(str(value)[:4]) +1) + (len(str(value)) - 4) * '0'
	return val

def samtools(dictionary, bam):
	labid = bam.split('_')[1]

	try:
		indexing = ['samtools', 'index', bam]
		print(' '.join(indexing))
		sub.call(indexing)
	except ValueError:
	 	print('Indexing BAM File Failed.')

	for variants in dictionary[labid]:

		attempt = False
		#raise ValueError('Samtools View Unable To Extract Region.')
		#try:
		chrom = str(variants[0])
		vstart = start_position(variants[1])
		vend = end_position(variants[2])
		extension = 'chr' + chrom + '-' + vstart + '-' + vend
		region = chrom + ':' + vstart + '-' + vend

		#print(vstart, vend, region)

		tmp_sam = bam.split('.')[0] + '.tmp.sam'
		extraction = ['samtools', 'view', '-h', bam, region]
		print(' '.join(extraction))
		with open(tmp_sam, 'w') as f:
			sub.call(extraction, stdout=f)
		#except:
		# 	print('Samtools View Unable To Extract Region.')
		# 	attempt = True

		if attempt:
			print('Attempting Second Extraction.')
			try:
				region = 'chr' + variants[0]
				tmp_sam = bam.split('.')[0] + '.tmp.sam'
				extraction = ['samtools', 'view', '-b', bam, region, '>', tmp_sam]
				print(' '.join(extraction))
				with open(tmp_sam, 'w') as f:
					sub.call(extraction, stdout=f)
			except:
				print('Samtools View Second Extraction Failed. Review BAM File.')
				exit()

		try:
			fbam = tmp_sam.split('.')[0] + '.' + extension + '.bam'
			conversion = ['samtools', 'view',  '-bS', tmp_sam]
			print(' '.join(conversion))
			with open(fbam, 'w') as f:
				sub.call(conversion, stdout=f)
		except:
			print('SAM to BAM Conversion Failed.')
			exit()

		try:
			indexing = ['samtools', 'index', fbam]
			print(' '.join(indexing))
			sub.call(indexing)
		except:
		 	print('Indexing BAM File Failed.')


def main():

	myargs = create_parser()
	input_file = myargs.input[0]
	bam = myargs.bam[0]
	#out = myargs.out[0]

	file_path = os.path.abspath(input_file)
	df = file_to_dataframge(file_path)

	info_dict = map_variants(df)
	samtools(info_dict, bam)



if __name__ == '__main__':
	main()
