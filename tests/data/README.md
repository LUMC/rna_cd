The `micro.bam` bam file was generated using data downloaded from ENA with
project number [ERR2438055](https://www.ebi.ac.uk/ena/data/view/ERR2438055).

It contains just under 16k reads of sample NA12878 (the Genome in a Bottle 
sample), on the mitochondrial genome. This was aligned on hg19 with minimap2,
and sorted duplicate marked with Picard. Then, about 1% of the total number of
reads on chrM was sampled to generate the `micro.bam` file.

`micro2.bam` derives from the same source, but is subsampled slightly slightly
differently, and includes only just more than 10k reads.    
