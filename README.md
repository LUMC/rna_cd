# RNA Contamination Detection

Detect contaminations of mouse or human RNA in human DNA Illumina reads. 

Mouse and human RNA contamination in a DNA sample gives a spike of reads with 
large amounts of softclips in chrM. This is likely due to an expressed 
mitochondrial gene. We can use this behaviour to detect the presence of mouse 
RNA in our data.

The mitochondrial chromosome is usually covered completely in both exome and
whole-genome sequencing experiments, and can thus be used for both approaches.

This tool has to be trained using a set samples known to be contaminated. 
We will possibly provide a pre-trained model in the future.  

## Requirements

* Python 3.6+
* click
* scikit-learn
* pysam

## License
AGPLv3