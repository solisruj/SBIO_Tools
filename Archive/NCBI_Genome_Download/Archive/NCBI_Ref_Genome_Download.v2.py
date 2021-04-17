#!/usr/bin/python

import pandas as pd
import re
import sys
import os
import subprocess
import argparse

# Function to parse command-line arguments.
def create_parser():
	parser = argparse.ArgumentParser(description="Downloads NCBI Files (Primarily GCF Files) in batch. This program will output genomic fasta files.")
	parser.add_argument("-a", "--assembly_file", dest="assembly_file", type=str, nargs=1 , help="This is an NCBI Downloaded assembly file. Use 'wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt' to get the latest file.", required=True)
	parser.add_argument("-in", "--input_file", dest="input_file", type=str, nargs=1, help="A text file List of Accession IDS for download.", required=True) 
	args = parser.parse_args()
	return args

def Get_FTP(bac_name, assembly_info):
	ftp = []
	for i in range(len(bac_name)):
		cmnd = 'grep \'' + bac_name[i] + '\' '+ assembly_info +' | awk -F "\\t" \'{print $20}\''  
		try:
			ftp_ = os.popen(cmnd).read()
			ftp.append(ftp_)
			print bac_name[i] + " Found"
		except:
			print bac_name[i] + " Not Found"
	return ftp

def get_genome(lst):
	for i in range(len(lst)):
		ftp_prts = lst[i].split('/')
		cmnd = 'wget -input genome_file ' + lst[i].rstrip('\n') + '/' + ftp_prts[9].rstrip('\n') + '_genomic.fna.gz'
		try:
			os.system(cmnd)
			print ftp_prts[9].rstrip('\n') + " Downloaded"
		except:
			print ftp_prts[9].rstrip('\n') + " Download Failed"

def clean_ftp(ftp_):
  ftp_cln = []
  for i in range(len(ftp_)):
    ftp_splt = ftp_[i].split('\n')
    for n in range(len(ftp_splt)):
      ftp_cln.append(ftp_splt[n])
  ftp_cln = filter(None, ftp_cln)
  return ftp_cln


def main():
		myargs = create_parser()
		file = myargs.input_file[0]
		assem = myargs.assembly_file[0]
		#file = sys.argv[1]
		#assem = sys.argv[2]
		bac_list = pd.read_table(file, header=None)
		bac_names = bac_list[0].values.tolist()
		ftp_list = Get_FTP(bac_names, assem)
		cln = clean_ftp(ftp_list)
		get_genome(cln)
		print "Downloads Completed"

if __name__ == '__main__':
	main()
