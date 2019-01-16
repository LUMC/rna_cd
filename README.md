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
* matplotlib

## Installation

`python setup.py install`

## Usage

### Training

```
Usage: rna_cd-train [OPTIONS]

Options:
  --chunksize INTEGER             Chunksize in bases. Default = 100
  -c, --contig TEXT               Name of mitochrondrial contig in your BAM
                                  files. Default = chrM
  -pd, --positives-dir DIRECTORY  Path to directory containing positive BAM
                                  files. Mutually exclusive with --positives-
                                  list
  -nd, --negatives-dir DIRECTORY  Path to directory containing negative BAM
                                  files. Mutually exlusive with --negatives-
                                  list
  -pl, --positives-list FILE      Path to file containing a list of paths to
                                  positive BAM files. Mutually exclusive with
                                  --positives-dir
  -nl, --negatives-list FILE      Path to file containing a list of paths to
                                  negative BAM files. Mutuallly exclusive with
                                  --negatives-dir
  --cross-validations INTEGER     Number of folds for cross validation run.
                                  Default = 3
  --verbosity INTEGER             Verbosity value for cross validation step.
                                  Default = 1
  -j, --cores INTEGER             Number of cores to use for processing of BAM
                                  files and cross validations. Default = 1
  --plot-out PATH                 Optional path to PCA plot.
  -o, --model-out PATH            Path where model will be stored.  [required]
  --help                          Show this message and exit.
```

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
AGPLv3