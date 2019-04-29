#!/usr/bin/env python3

# Importing in modules.
import pandas as pd
import argparse

# Function to parse command-line arguments.
def create_parser():
	parser = argparse.ArgumentParser(description="Provides the frequency of A, T, G, C bases in a sequence fragement. The program also returns the A/T and G/C ratios of the fragment sequence. In addition, this program also returns the total frequency of all the bases and the total A/T and G/C ratios of multiple sequences in an assembly.")
	parser.add_argument("-in", "--input_fasta", dest="input_fasta", type=str, nargs=1 , help="Input fasta file. This can be an assembly, or sequence in base format.", required=True)
	parser.add_argument("-out", "--output_file", dest="output_file", type=str, nargs=1, help="Name of the output summary file.", required=True) 
	args = parser.parse_args()
	return args

# Fucntion that reads through the input file and loads the sequences into a dictionary.
def sequence_to_dictionary(file_name):
	sequence_dict = {}
	with open(file_name) as f:
		for line in f.readlines():
			#print line.strip('\n')
			if('>' in line):
				header = line.strip('\n')
				sequence = ''
			if('>' not in line):
				fragement = line
				sequence += fragement.strip('\n')
			sequence_dict[header] = sequence
	return sequence_dict

# This function writes individual contig/sequence stats and the overal sequence stats to an output file.
def sequence_summary(sequence_dictionary, outfile):
	output_file = open(outfile, "w")
	total_assembly_summary = []
	output_file.write("Sequence_Header\tFreq_Adenine\tFreq_Thymine\tFreq_Cytosine\tFreq_Guanine\tLength\tA/T_Ratio\tG/C_Ratio\n")
	for header in sequence_dictionary:
		length = len(sequence_dictionary[header])
		freq_Adenine = sequence_dictionary[header].count('A')
		freq_Thymine = sequence_dictionary[header].count('T')
		freq_Cytosine = sequence_dictionary[header].count('C')
		freq_Guanine = sequence_dictionary[header].count('G')
		ratio_purine = float(freq_Adenine + freq_Thymine) / float(length)
		ratio_pyrimidine = float(freq_Cytosine + freq_Guanine) / float(length)
		seq_stat = header+"\t"+str(freq_Adenine)+"\t"+str(freq_Thymine)+"\t"+str(freq_Cytosine)+"\t"+str(freq_Guanine)+"\t"+str(length)+"\t"+str(round(ratio_purine,4))+"\t"+str(round(ratio_pyrimidine,4))+"\n"
		output_file.write(seq_stat)
		stat_information = freq_Adenine, freq_Thymine, freq_Cytosine, freq_Guanine, length
		total_assembly_summary.append(stat_information)
	total_assembly_summary_df = pd.DataFrame(total_assembly_summary)
	total_assembly_stat = []
	for col in range(len(total_assembly_summary_df.columns)):
		total_assembly_stat.append(total_assembly_summary_df.iloc[:,col].sum())
	total_ratio_purine = float(total_assembly_stat[0] + total_assembly_stat[1]) / float(total_assembly_stat[4])
	total_ratio_pyrimidine = float(total_assembly_stat[2] + total_assembly_stat[3]) / float(total_assembly_stat[4])
	output_file.write('\n')
	output_file.write("Total_Freq_Adenine\tTotal_Freq_Thymine\tTotal_Freq_Cytosine\tTotal_Freq_Guanine\tTotal_Length\tTotal_A/T_Ratio\tTotal_G/C_Ratio\n")
	total_seq_stats = str(total_assembly_stat[0])+"\t"+str(total_assembly_stat[1])+"\t"+str(total_assembly_stat[2])+"\t"+str(total_assembly_stat[3])+"\t"+str(total_assembly_stat[4])+"\t"+str(round(total_ratio_purine,4))+"\t"+str(round(total_ratio_pyrimidine,4))+"\n"
	output_file.write(total_seq_stats)
	output_file.close()

# The main body of the program.
def main():
	myargs = create_parser()
	in_file = myargs.input_fasta[0]
	out_file = myargs.output_file[0]
	seq_dict = sequence_to_dictionary(in_file)
	sequence_summary(seq_dict, out_file)


if __name__ == '__main__':
	main()
