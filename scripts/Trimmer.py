import sys

trim_start = sys.argv[1]
trim_trailing = sys.argv[2]
fasta_file = sys.argv[3]
outfile = sys.argv[4]

contigs = {}
for line in open(fasta_file, 'r'):
	if (">" in line):
		header = line
		seq = ''
	elif (">" not in line):
		s = line.strip("\n")
		seq += s
	contigs[header] = seq

output = open(outfile, 'w')

for header in contigs.keys():
	trim_end = len(contigs[header]) - int(trim_trailing)
	output.write(header)
	trimmed_seq = contigs[header][int(trim_start):int(trim_end)]
	for n in xrange(0,len(trimmed_seq), 80):
		output.write(str(trimmed_seq[n:n+80])+"\n")

output.close()
