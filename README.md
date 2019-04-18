# Simple Bioinformatic Tools (SBIO_Tools)
SBIO Tools are simple python bioinformatic scripts and notebooks written by me to perform simple bioinformatic analysis. Links references will be provided for external programs, and material used to either pull simple genome assembly stats or create fast and ready graphs using the pythons seaborn module.

# 16s
Is a folder containing a markdown notebook that shows how to align extracted 16s rRNA sequences and build a simple tree for the sequences.

# Average Identity
Is a folder containing a jupyter and markdown notebook that shows how to use average identity scripts for nucleotide and amino acids. ANI and AAI sub-folders contain example outputs and graphs that can be created with programs found in scripts folder.

# NCBI Genome Download
Is a script that uses NCBI's FTP to download genomic information (e.g. genbank, fasta, faa, etc). Because NCBI is used widely by many
researchers. It is good to limit downloads or downloading information when their is minimum activity on the site. 

# Scripts
Contains basic scripts to pull information.

### Average Nucleotide Identity (Single Run):
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires blastn.
### Average Nucleotide Identity w/ References (ANIRs):
* Requires Average Nucleotide Identity to be exported to path.
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires blastn.
* ANIRs folder for exmaple notebook.
### Average Amino Identity (Single Run):
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires blastp.
* One way blast. 
* (Reciprocal blast comming soon).
### Averge Amino Identity w/ References (AAIRs):
* Requires Average Amino Identity to be exported to path.
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires tblastp.
* One way blast. 
* (Reciprocal blast comming soon)
### Extract Sequences:
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
### Additional Scripts:
* DNA_Complementary.py
* DNA_Nucleotide_Counter.py
* DNA_to_RNA.py
* Extract_Fasta_from_Genbank.py
* Extract_Protein_From_Genbank.py
* Fragment_Sequence.py
* Prodigal_gff_fna_to_Genbank.py
* Re_Array.py
* Replace_String.py
* Sort_Average_Identity_Output.py

# Graphing
Contains basic scripts with textual user interfaces for quick graphing.
* Barplot.py
* Boxplot.py
* Dendrogram_Heatmap.py
* Heatmap.py
* Hexbin_plot.py
* Histogram.py
* Scatterplot_Matrix.py
* Scatter_plot.py
* Simple_Regression_plot.py
