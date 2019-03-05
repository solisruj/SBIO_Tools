# SBIO_Tools
SBIO Tools are simple python bioinformatic tools written by me to either pull simple genome assembly stats or create fast and ready graphs
using the pythons seaborn module.

# NCBI Genome Download
Is a script that uses NCBI's FTP to download genomic information (e.g. genbank, fasta, faa, etc). Because NCBI is used widely by many
researchers. It is good to limit downloads or downloading information when their is minimum activity on the site. 

# Scripts
Contains basic scripts to pull information.

### Average Nucleotide Identity:
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires blastn.
### Extract Sequences:
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
### Average Amino Identity (COMMING SOON):
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires tblastn.

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
* Sort_ANI_Output.py

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

# Note
Due to python 2.7 being discontinued in 2020. All programs will be transcribed to python 3. New scripts will also be written in python 3. If not, I will eventually get to them. This shouldn't cause many issues, since there are onyl minor syntax changes.
