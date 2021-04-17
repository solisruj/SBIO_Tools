#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import collections
import statistics
import argparse

def create_parser():
	parser = argparse.ArgumentParser(description="This program takes in a read dataset and outputs Number of bases and the mode N location in a text file, saves a GC_Content and Quality Score PNG file.")
	parser.add_argument("-r", dest="reads", type=str, nargs=1 , help="Input Read dataset.", required=True)
	parser.add_argument("-o", dest="output", type=str, nargs=1, help="Name of the output files.", required=True) 
	args = parser.parse_args()
	return args

# Function converts the phred score to a numerical quality score.
def phred33ToQ(qual):
	return ord(qual) - 33

# Function reads a fastq file and parses the sequences and qualities.
def readFastq(filename):
	sequences = []
	qualities = []
	with open(filename) as fh:
		while True:
			fh.readline()  # skip name line
			seq = fh.readline().rstrip()  # read base sequence
			fh.readline()  # skip placeholder line
			qual = fh.readline().rstrip() # base quality line
			if len(seq) == 0:
				break
			sequences.append(seq)
			qualities.append(qual)
	return sequences, qualities

# Function gets the average GC content at each base position within a read dataset. 
def findGCByPos(reads):
	gc = [0] * len(reads[0])
	totals = [0] * len(reads[0])
	N_loc = []
	for read in reads:
		for i in range(len(read)):
			if (read[i] == 'C' or read[i] == 'G'):
				gc[i] += 1
			totals[i] += 1
			if (read[i] == 'N'):
				N_loc.append(i)
	for i in range(len(gc)):
		if totals[i] > 0:
			gc[i] /= float(totals[i])
	return gc, N_loc

# Function gets the average quality score at each base position within a read dataset. 
def createHist(qualities):
	hist_q = [0] * len(qualities[0])
	hist_t = [0] * len(qualities[0])
	for qual in qualities:
		for i in range(len(qual)):
			hist_q[i] += phred33ToQ(qual[i])
			hist_t[i] += 1
	for i in range(len(hist_q)):
		if hist_t[i] > 0:
			hist_q[i] /= float(hist_t[i])
	return hist_q





def main():

	myargs = create_parser()
	file = myargs.reads[0]
	out = myargs.output[0]

	sequences, qualities = readFastq(file) 

	count = collections.Counter()
	for seq in sequences:
		count.update(seq)

	bar = plt.figure(1)
	h = createHist(qualities)
	plt.title('Average Quality Score In Read Dataset')
	plt.xlabel('Base Position in Read')
	plt.ylabel('Quality Score')
	plt.bar(range(len(h)), h)
	plt.savefig(out + '_Quality_Score.png')

	gc, N_loc = findGCByPos(sequences)
	output = open(out + '.txt', 'w')
	output.write('Base Countes:\nC: ' + str(count['C']) + '\nG: ' + str(count['G']) + '\nA: ' + str(count['A']) + '\nT: ' + str(count['T']) + '\n')
	output.write('Mode N Location:' + str(statistics.mode(N_loc)) +'\n')
	output.write('Left N Location:' + str(min(N_loc)) +'\n')
	output.write('Right N Location:' + str(max(N_loc)) +'\n')
	output.close()

	line = plt.figure(2)
	plt.title('Average GC Content In Read Dataset')
	plt.xlabel('Base Position in Read')
	plt.ylabel('GC Content')
	plt.plot(range(len(gc)), gc)
	plt.savefig(out + '_GC_Content.png')

if __name__ == '__main__':
	main()