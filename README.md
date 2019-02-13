[![Build Status](https://travis-ci.org/LUMC/rna_cd.svg?branch=master)](https://travis-ci.org/LUMC/rna_cd) [![codecov](https://codecov.io/gh/LUMC/rna_cd/branch/master/graph/badge.svg)](https://codecov.io/gh/LUMC/rna_cd)
# RNA Contamination Detection

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
uncontaminated ("negative") groups.
## Requirements

* Python 3.5+
* click
* scikit-learn
* pysam
* matplotlib

## Installation

`python setup.py install`

## Usage

### Training



For example:

```bash
rna_cd-train -pl pos.list -nl neg.list -j 8 --plot-out out.png -o model.out
```

### Classification

```
Usage: rna_cd-classify [OPTIONS]

Options:
  --chunksize INTEGER        Chunksize in bases. Default = 100
  -c, --contig TEXT          Name of mitochrondrial contig in your BAM files.
                             Default = chrM
  -j, --cores INTEGER        Number of cores to use for processing of BAM
                             files. Default = 1
  -d, --directory DIRECTORY  Path to directory with BAM files to be tested.
                             Mutually exclusive with --list-items
  -l, --list-items FILE      Path to file containing list of paths to BAM
                             files to be tested. Mutually exclusive with
                             --directory
  -m, --model FILE           Path to model.
  -o, --output PATH          Path to output file containing classifications.
                             [required]
  --help                     Show this message and exit.
```

For example:

```bash
rna_cd-classify -m model.out -l samples.list -j 8 -o pred.out 
```

## License
AGPLv3+