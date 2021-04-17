#!/usr/bin/env python3

import argparse
import os

def create_parser():
	parser = argparse.ArgumentParser(description="This program provides simple sequence comparison of a set of sequences: hamming_distance (hd), transitions/transversions (ttr), distance matrix (mtx), edit distance (ed).")
	parser.add_argument("-in", "--input", dest="input", type=str, nargs=1 , help="Input fasta file containing sequences for comparison.", required=True)
	parser.add_argument("-type", "--type", dest="type", type=str, nargs=1 , help="Option types: hd, ttr, mtx, ed", required=True)
	#parser.add_argument("-out", "--output", dest="output", type=str, nargs=1, help="Name of the output file.", required=True) 
	args = parser.parse_args()
	return args

def hamming_distance(seq_1, seq_2):
	errors = 0
	if (len(seq_1) == len(seq_2)):
		for x in range(len(seq_1)):
			if(seq_1[x] != seq_2[x]):
				errors += 1
	else:
		print('Sequences are of unequal length.')
	return errors

def transitions_and_transversions(seq_1, seq_2):
	transitions = 0
	transversions = 0
	status = {'G' : {'A': 0, 'T': 1, 'C': 1}, 
		'A' : {'G': 0, 'T': 1, 'C': 1},
		'T' : {'C': 0, 'A': 1, 'G': 1},
		'C' : {'T': 0, 'A': 1, 'G': 1}}
	if (len(seq_1) == len(seq_2)):
		for x in range(len(seq_1)):
			if(seq_1[x] != seq_2[x]):
				if (status[seq_1[x]][seq_2[x]] == 0):
					transitions += 1
				elif(status[seq_1[x]][seq_2[x]] == 1):
					transversions += 1
	else:
		print('Sequences are of unequal length.')
	return transitions, transversions, round(transitions/transversions,11)

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

# The variable passed must be a dictiobnary of reads.
def p_distance_matrix(reads):
	p_distance = []
	read_length = len(reads[1][1])
	length = len(reads) 
	for i in range(1, length+1):
		for j in range(1, length+1):
			pd = float(hamming_distance(reads[i][1], reads[j][1])) / float(read_length)
			p_distance.append('{:.5f}'.format(pd))
	for i in range(length):
		print(" ".join(p_distance[i*4:(i+1)*4]))

def matrix_sequence(matrix):
	result = []
	l = len(matrix)
	j = len(matrix[0])
	for i in range(l):
		if ( i < (l/2)):
			result.append(sum(matrix[i][0:int(j/2)]))
		elif ( i >= (l/2)):
			result.append(sum(matrix[i][int(j/2):j]))
	return result

def edit_distance(seq_1, seq_2):
	e_matrix = []
	for i in range(len(seq_2)):
		e_matrix.append([0]*(len(seq_1)))

	for i in range(len(seq_2)):
		for j in range(len(seq_1)):
			if (seq_2[i] == seq_1[j]):
				e_matrix[i][j] = 1
	tranposed_matrix = list(map(list, zip(*e_matrix)))
	vector = matrix_sequence(tranposed_matrix)
	print('Edit distance:', vector.count(0))
	print(vector)

	aligned_seq = ''
	for i in range(len(vector)):
		if(vector[i] == 1):
			aligned_seq += seq_1[i]
		else:
			aligned_seq += '-'

	print(seq_1)
	print(aligned_seq)


def main():

	myargs = create_parser()
	infile = myargs.input[0]
	file_type = myargs.type[0]
	#output = myargs.output[0]

	reads = parse_fasta_file(infile)

	if ('hd' == file_type):
		for n in range(1,len(reads)):
			distance = hamming_distance(reads[n][1], reads[n+1][1])
			print('Contig Comparison: ', reads[n][0], reads[n+1][0])
			print('Hamming distance:', distance)

	if ('ttr' == file_type):
		for n in range(1,len(reads)):
			trans_status = transitions_and_transversions(reads[n][1], reads[n+1][1])
			print('Contig Comparison: ', reads[n][0], ',', reads[n+1][0])
			print('Transitions: ', trans_status[0])
			print('Transversions: ', trans_status[1])
			print('Ratio: ', trans_status[2])

	if ( 'mtx' == file_type):
		print('Distance Matrix of Sequences:')
		p_distance_matrix(reads)


	if ( 'ed' == file_type):
		for n in range(1,len(reads)):
			print('Contig Comparison: ', reads[n][0], reads[n+1][0])
			edit_distance(reads[n][1], reads[n+1][1])


if __name__ == '__main__':
	main()
