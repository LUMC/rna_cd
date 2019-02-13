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

.. click:: rna_cd.cli:train_cli
    :prog: rna_cd-train
    :show-nested:
