
# Bacterial GWAS SNP Calling with MUMmer

[MUMmer](http://mummer.sourceforge.net/manual/#introduction) is software for rapid alignment of very large DNA and amino acid sequences. It is overall very modular and versatile, and relies on a suffix tree data structure for efficient pattern matching. Due to MUMmers versatile and modular components, one can knit together a SNP detection pipeline (covered in the manuel).

**References**

Open source MUMmer 3.0 is described in "Versatile and open software for comparing large genomes." S. Kurtz, A. Phillippy, A.L. Delcher, M. Smoot, M. Shumway, C. Antonescu, and S.L. Salzberg, Genome Biology (2004), 5:R12.

MUMmer 2.1, NUCmer, and PROmer are described in "Fast Algorithms for Large-scale Genome Alignment and Comparision." A.L. Delcher, A. Phillippy, J. Carlton, and S.L. Salzberg, Nucleic Acids Research (2002), Vol. 30, No. 11 2478-2483.

MUMmer 1.0 is described in "Alignment of Whole Genomes." A.L. Delcher, S. Kasif, R.D. Fleischmann, J. Peterson, O. White, and S.L. Salzberg, Nucleic Acids Research, 27:11 (1999), 2369-2376.

Space efficent suffix trees are described in "Reducing the Space Requirement of Suffix Trees." S. Kurtz, Software-Practice and Experience, 29(13): 1149-1171, 1999.

**Acknowledgments**

The development of MUMmer is supported in part by the National Science Foundation under grants IIS-9902923 and IIS-9820497, and by the National Institutes of Health under grants R01-LM06845 and N01-AI-15447.
Thanks to SourceForge for the fantastic service!

MUMmer3.0 is a joint development effort by Stefan Kurtz of the University of Hamburg and Adam Phillippy, Art Delcher and Steven Salzberg at TIGR. Stefan's contribution of the new suffix tree code was essential to making MUMmer 3.0 an open source project. Also thanks to Corina Antonescu for the development of mapview.

#### Aligning Nucleotide Sequences:


```python
# Alignment of closley related nucleotide sequences.
nucmer --prefix=<reference query abbreviation> <reference fasta> <query fasta>
```

#### Filtering Delta File:


```python
# This is done to remove conflicting repeat copies.
# Filtering the information based on the various command line switches, outputting only the desired alignments to stdout
delta-filter -r -q <reference query delta file> > <reference query filter file>
```

#### SNP Calling:


```python
# Reporting polymorphisms contained in a delta encoded alignment file.
show-snps -TClr -x 1 <reference query filter file> > <reference query .snps>
```
