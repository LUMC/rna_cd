Training
========

To train the support vector machine, you need a set of contaminated
("positive") and a set of uncontaminated ("negative") BAM files. For each
category, you can organize your BAM files in two distinct ways:

1. Place all BAM files of the category in the same directory.
2. Make a flat text file, where each line points to a path of a BAM file.

.. note:: Your BAM files must be indexed.

Once you have this in place, you need to choose the contig in your BAM file
that you want to collect metrics for, and the chunksize. rna_cd will split
your contig of interest in chunks with a maximum size ``chunksize``, and
collect a number of metrics for each chunk. When you later use the model for
classifications you **must** use the same contig and chunksize as you used
during the training step.

In our hands, the mitochondrial contig, at a chunksize of 100 bases, gives
enough information to be trainable. When choosing the mitochondrial contig,
one also benefits from its small size, which makes the training step fast.

Training can work in multicore mode. When using multiple cores, you will
process multiple BAM files simultaneously. This can drastically speed up
the metric collection for large numbers of BAM files.

Lastly, you have to set the amount of fold cross validations. By default this
is 3, but you may set it to any positive integer.

The created model will saved to disk as a JSON file. The JSON file contains
the pickled model.

Optionally, you can save a plot of the top two principal components of the
training samples to disk.


Examples
--------

Directory method, chrM, chunksize = 100, cores = 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    rna_cd-train -c chrM -pd positives_dir -nd negatives_dir -j 3 \
    --chunksize 100 -o model.json


List method, chrM, chunksize = 100, cores = 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    rna_cd-train -c chrM -pl positives.list -nl negatives.list -j 3 \
    --chunksize 100 -o model.json


List method, chrM, chunksize = 100, cores = 3, with plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    rna_cd-train -c chrM -pl positives.list -nl negatives.list -j 3 \
    --chunksize 100 -o model.json --plot-out pca.png


Usage
-----

::

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
