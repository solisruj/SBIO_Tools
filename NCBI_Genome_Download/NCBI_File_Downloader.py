#!/usr/bin/python

import pandas as pd
import re
import sys
import os
import subprocess
import argparse

# Function to parse command-line arguments.
def create_parser():
	parser = argparse.ArgumentParser(description="Downloads NCBI Files in batch to the working directory.")
	parser.add_argument("-a", "--assembly_file", dest="assembly_file", type=str, nargs=1 , help="This is an NCBI Downloaded assembly file. Use 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt' to get the latest file.", required=True)
	parser.add_argument("-i", "--input_file", dest="input_file", type=str, nargs=1, help="A text file List of IDS for download from NCBI.", required=True) 
	parser.add_argument("-ft", "--file_type", dest="file_type", type=str, nargs=1, help="File type to download options: report, stats, cds, fcnt, ftble, fna, gbff, gff, faa, gpff, rna, tcds, wgsmaster, annotation_hashes, assembly_status, md5checksums", required=True)
	parser.add_argument("-id", "--id_type", dest="id_type", type=str, nargs=1, help="ID type option: GCF, GCA, ASM, species", required=True) 
	args = parser.parse_args()
	return args

# Function that parses an NCBI assembly file, and returns a specific map depending on the map type. 
def map_assembly(assembly_file, map_type):
	# Setting some empty dictionary variables.
	GCF_map = {}
	GCA_map = {}
	ASM_map = {}
	species_map = {}
	# Reading over the assembly file to parse it. 
	for line in open(assembly_file, 'rb'):
		# If statements not to capture '# ' pattern and rows less than size 12 (these rows do not have NCBI ftp link).
		if("# " not in line):
			row = line.split("\t")
			if (len(row) > 12):
				# Capturing only complete genomes. This can be later changed to an input variable to include other types.
				#	This step also captures the ftp link and ID type (e.g. GCF, GCA, ASM).
				if ('Complete Genome' == row[11] or 'Contig' == row[11]):
					GCF_map[row[0]] = row[19]
					GCA_map[row[17]] = row[19]
					ASM_map[row[15]] = row[19]
					if (map_type == 'species'):
						if (row[7].split(' ')[0] not in species_map):
							species_map[row[7].split(' ')[0]] = [row[19]]
						elif (row[7].split(' ')[0] in species_map.keys()):
							species_map[row[7].split(' ')[0]].append(row[19])
			else:
				pass
	# Returning the map type based on map_type. 
	if (map_type == 'GCF'):
		return GCF_map
	elif (map_type == 'GCA'):
		return GCA_map
	elif (map_type == 'ASM'):
		return ASM_map
	elif (map_type == 'species'):
		return species_map

# Function to get ftp list from mapped ftp dictionary. Gives Error message if ID not found. 
def get_ftps(id_list, map_dict):
	ftps = []
	for ID in id_list:
		if (ID not in map_dict.keys()):
			print "Error: "+ ID + " ID might not be in the NCBI assembly list file. Download new assembly information file."
			print "Use 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt' to get a more recent file."
		elif (ID in map_dict.keys()):
			ftps.append(map_dict[ID])
	return ftps

# Function to call the file type from NCBI. 
def get_file(ftps, file_type):
	for i in range(len(ftps)):
		ftp_path_items = ftps[i].split('/')
		if (file_type == 'report'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_assembly_report.txt']
		if (file_type == 'stats'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_assembly_stats.txt']
		if (file_type == 'cds'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_cds_from_genomic.fna.gz']
		if (file_type == 'fcnt'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_feature_count.txt.gz']
		if (file_type == 'ftble'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_feature_table.txt.gz']
		if (file_type == 'fna'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_genomic.fna.gz']
		if (file_type == 'gbff'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_genomic.gbff.gz']
		if (file_type == 'gff'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_genomic.gff.gz']
		if (file_type == 'faa'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_protein.faa.gz']
		if (file_type == 'gpff'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_protein.gpff.gz']
		if (file_type == 'rna'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_rna_from_genomic.fna.gz']
		if (file_type == 'tcds'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_translated_cds.faa.gz']
		if (file_type == 'wgsmaster'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + '_wgsmaster.gbff.gz']
		if (file_type == 'annotation_hashes'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + 'annotation_hashes.txt']
		if (file_type == 'assembly_status'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + 'assembly_status.txt']
		if (file_type == 'md5checksums'):
			cmnd = ['wget', ftps[i] + '/' + ftp_path_items[9]  + 'md5checksums.txt']
		print "Command Called: ", ' '.join(cmnd)
		# Try/Except catch to try and get file. Prints error if failed. 
		try:
			subprocess.call(cmnd)
			print ftp_path_items[9] + " Downloaded"
		except:
			print "Error: " + ftp_path_items[9] + " Download Failed"

def main():
		# Getting command-line arguments. 
		myargs = create_parser()
		file_input = myargs.input_file[0]
		assembly_file = myargs.assembly_file[0]
		option = myargs.file_type[0]
		id_option = myargs.id_type[0]

		file_options = ['report', 'stats', 'cds',
				'fcnt','ftble', 'fna', 'gbff',
				'gff', 'faa', 'gpff', 'rna', 
				'tcds', 'wgsmaster', 'annotation_hashes',
				'assembly_status', 'md5checksums']

		id_type = ['GCF', 'GCA', 'ASM', 'species']

		# Reading in the ID_list and converting it to a list. 
		ID_list = pd.read_table(file_input, header=None)
		ID_list = ID_list[0].values.tolist()

		# Mapping the NCBI's assembly information file.
		if (id_option in id_type):
			map_dictionary = map_assembly(assembly_file, id_option)
		else:
			print "Error: ", id_option, "is not a valid file type option"
			print "For help see menu: NCBI_File_Downloader.py -h"
		
		# Getting the a list of NCBI ftp core link.
		ftp_list = get_ftps(ID_list, map_dictionary)

		# Get the file type based on the file option. 
		if (option in file_options):
			get_file(ftp_list, option)
		else:
			print "Error: ", option, "is not a valid file type option"
			print "For help see menu: NCBI_File_Downloader.py -h"

		print "Downloads Completed"

if __name__ == '__main__':
	main()





