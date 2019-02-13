Introduction
============

Human DNA-seq experiments may be contaminated with RNA. This usually
negatively influences downstream analysis. For example, it can introduce
false positive variants around splice sites, suppress alternative alleles
due to allele-specific expression, and alter coverage patterns which may then
influence CNV calling. Moreover, it is typically hard to detect.

Modern Illumina sequencers unfortunately are more prone to such contamination,
as the very large capacity of novaseq sequencers typically means multiple
projects are sequenced on the same flowcells. Combined with the increased risk
of index hopping in novaseq sequencers, this alltogether means that
cross-contamination of samples is more likely - including contamination of
RNA into DNA-seq experiments.

rna_cd is a python package and command line tool designed to detect such
RNA contamination of DNA-seq experiments. It uses the altered coverage
and softclip patterns in contaminated samples to train a Support Vector
Machine that can classify BAM files into contaminated ("positive") and
uncontamined ("negative") groups.
