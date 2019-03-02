#!/usr/bin/env python

import sys, os, argparse
from Bio import GenBank, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.SeqFeature import SeqFeature, FeatureLocation

# Creates a tui parser for command line use. 
def create_parser():
	parser = argparse.ArgumentParser(description="Creates a genbank file from prodigal gff and fasta file. Note: Prodigal outputs a genbank file as well. This was created as an alternative purpose.")
	parser.add_argument("-gff", "--gff", dest="gff", type=str, nargs=1 , help="Prodigal gff tab deliminated file.", required=True)
	parser.add_argument("-fna", "--fna", dest="fasta", type=str, nargs=1, help="Associated fasta file to the gff file.", required=True)
	parser.add_argument("-id", "--id", dest="id", type=str, nargs=1, help="Associated ID.", required=True) 
	parser.add_argument("-out", "--out", dest="out", type=str, nargs=1, help="Name of the output genbank file.", required=True) 
	args = parser.parse_args()
	return args

# This function returns a map file of an input prodigal gff file.
def map_prodigal_gff(input_file):
	prodical_map = {}
	for line in open(input_file, 'r'):
		if ('#' not in line):
			col = line.strip('\n').split('\t')
			if ( col[0] not in prodical_map.keys()):
				prodical_map[col[0]] = [ [col[1], col[2], col[3], col[4], col[5], col[6], col[7], col[8] ] ]
			elif(col[0] in prodical_map.keys()):
				CDS = [col[1], col[2], col[3], col[4], col[5], col[6], col[7], col[8]]
				prodical_map[col[0]].append(CDS)
	return prodical_map


def main():

	# Input variables from created parser.
	myargs = create_parser()
	prodigal_gff = myargs.gff[0]
	prodigal_fasta = myargs.fasta[0]
	ID = myargs.id[0]
	output = myargs.out[0]

	# Calling the map prodigal gff function and opening the output file for writing.
	gff_dict = map_prodigal_gff(prodigal_gff)
	output_file = open(output, 'w')

	# Main loop to parse the fasta file. It also creates a genbank record for each contig in the fasta file. 
	for contig in SeqIO.parse(prodigal_fasta, "fasta"):
		contig_header = contig.description 
		sequence_string = str(contig.seq)

		if (contig_header in gff_dict.keys()):
			sequence_object = Seq(sequence_string, IUPAC.unambiguous_dna)
			record = SeqRecord(sequence_object, id=contig_header, name=ID, description="")
		
			# Adding Annotations.
			for CDS in gff_dict[contig_header]:
				info = CDS[7].split(';')
				print ">" + contig_header, CDS[2], CDS[3]
				feature = SeqFeature(FeatureLocation(start=int(CDS[2]), end=int(CDS[3])), type=CDS[1])
				record.features.append(feature)
				feature.qualifiers['genename'] = ""
				feature.qualifiers['genepredictionid'] = info[0].split("=")[-1]
				feature.qualifiers['locus_tag'] = contig_header + '_' + info[0].split('_')[-1]
				if (CDS[5] == '+'):
					feature.qualifiers['orientation'] = 1
				if (CDS[5] == '-'):
					feature.qualifiers['orientation'] = -1
				feature.qualifiers['seqname'] = contig_header + '_' + info[0].split('_')[-1]
				feature.qualifiers['source_id'] = ID
				feature.qualifiers['startpos'] = CDS[2]
				feature.qualifiers['endpos'] = CDS[3]
				feature.qualifiers['note'] = CDS[0] + " prediction with score of " + CDS[4]
				coding_dna = Seq(feature.extract(sequence_string), IUPAC.unambiguous_dna)
				feature.qualifiers['translation'] = Seq.translate(coding_dna)
				print Seq.translate(coding_dna)

			# Writing record to ouput genbank. 
			SeqIO.write(record, output_file, 'genbank')
		else:
			# If the contig doesnt have any predicted CDS then it passes it straight to a record.
			sequence_object = Seq(sequence_string, IUPAC.unambiguous_dna)
			record = SeqRecord(sequence_object, id=contig_header, name=ID, description=contig_header)
			SeqIO.write(record, output_file, 'genbank')

if __name__ == "__main__":
	main()