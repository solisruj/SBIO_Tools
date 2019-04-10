# Simple Bioinformatic Tools (SBIO_Tools)
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
### Average Nucleotide Identity w/ References (ANIRs):
* Requires Average Nucleotide Identity to be exported to path.
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires blastn.
* ANIRs folder for exmaple notebook.
### Average Amino Identity:
* Requires the NCBI toolkit to be installed (bin is exported to path).
* Requires makeblastdb.
* Requires tblastn.
* One way tblastn. 
* (Reciprocal blast comming soon).
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
