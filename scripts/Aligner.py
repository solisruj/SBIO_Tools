#!/usr/bin/env python3

import sys

def global_alignment(seq_1, seq_2):
	if (len(seq_1) > len(seq_2)):
		seq_1, seq_2 = seq_2, seq_1

	# Set a dictionary of nucleotide scores.
	base_score = {
		'A' : {'A': 2 ,'C': -1 ,'G': 1, 'T':-1},
		'C' : {'A': -1 ,'C': 2 ,'G': -1, 'T':1},
		'G' : {'A': 1 ,'C': -1 ,'G': 2, 'T':-1},
		'T' : {'A': -1 ,'C': 1 ,'G': -1, 'T':2},
	}

	gap_score = -2

	# Initializing the alignment matrix.
	aln_mantrix = []
	for i in range(len(seq_1) + 1):
		row = []
		for j in range(len(seq_2) + 1):
			row.append(0)
		aln_mantrix.append(row)

	# Filling up the top row of list array.
	for i in range(len(aln_mantrix[0])):
		#print(i * -2)
		aln_mantrix[0][i] = i * -2

	# Filling up the first column of list array.
	for i in range(len(aln_mantrix)):
		#print(i * -2)
		aln_mantrix[i][0] = i * -2

	# Adding alignment scores to the aln_matrix.
	for i in range(1,len(seq_1)+1):
		for j in range(1,len(seq_2)+1):
			match = aln_mantrix[i-1][j-1] + base_score[ seq_1[i-1] ][ seq_2[j-1] ]
			gaps = aln_mantrix[i][j-1] + gap_score
			gapt = aln_mantrix[i-1][j] + gap_score
			aln_mantrix[i][j] = max(match, gaps, gapt)

	# Getting the overall alignment score.
	gl_score =  aln_mantrix[len(seq_1)][len(seq_2)]

	# Setting variables (to create the aligned sequences)
	alignment1 = ''
	alignment2 = ''
	i = len(seq_1)
	j = len(seq_2)

	# Re-creating the alignments by traceback.
	while (i > 0 and j > 0):
		if (aln_mantrix[i-1][j-1] == aln_mantrix[i][j] - base_score[ seq_1[i-1] ][ seq_2[j-1] ]):
			alignment1 += seq_1[i-1]
			alignment2 += seq_2[j-1]
			i = i - 1
			j = j - 1
		elif (aln_mantrix[i][j - 1] == aln_mantrix[i][j] - gap_score):
			alignment2 += seq_2[j - 1]
			alignment1 += '-'
			j = j - 1
		elif (aln_mantrix[i-1][j] == aln_mantrix[i][j] - gap_score):
			alignment2 += '-'
			alignment1 += seq_1[i-1]
			i = i - 1

	# Returning the lengths, alignment matrix, global alignment score, and aligned sequnces.
	return len(seq_2), len(seq_1), aln_mantrix, gl_score, alignment2, alignment1

def parse_fasta_file(file):

	reads = {}
	count = 0
	
	for line in open(file, 'r'):
		line = line.strip('\n')
		if ( '>' in line):
			header = line
			seq = ''
			count += 1
		elif ('>' not in line):
			seq = line
		reads[count] = [header, seq]
	
	return reads


def main():

	fasta_file = sys.argv[1]
	reads = parse_fasta_file(fasta_file)

	for n in range(1,len(reads)):
		aln_info = global_alignment(reads[n][1], reads[n+1][1])
		print(reads[n][0], '| length=',aln_info[0])
		print(aln_info[-2])
		print(reads[n+1][0], '| length=',aln_info[1])
		print(aln_info[-1])

'''
	seq_1 = 'ACGGTAG'
	seq_2 = 'CCTAAG'


	aln_info = global_alignment(seq_1, seq_2)

	print(aln_info[-2],"\n",aln_info[-1], aln_info[0],"\n",aln_info[1])
'''

main()