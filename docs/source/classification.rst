Classification
==============

As with the training step, you can organize your BAM files in two distinct
ways:

1. Place all BAM files of the category in the same directory.
2. Make a flat text file, where each line points to a path of a BAM file.

This time, there are no separate categories, as all BAM files are
a-priori unknown.

.. note:: Your BAM files must be indexed.

.. warning:: As mentioned before, you **must** use the **exact** same contig
             and chunksize settings in this step as were used during the
             training step.

As with the training step, metric collection can run in multicore mode
during classifcation as well.

Once you have prepared your BAM files, and chosen your parameters, you will
use the model you generated during the training step to classify your
BAM files into contaminated ("positive") and uncontamined ("negative")
groups.

Additionally, there is an optional third category with label "unknown". This
represents samples for which we are unsure to which category they belong
to. By default, samples are categorized as "unknown" when the class
probability of the most likely category is below 0.75. You can override this
parameter, but it must be higher than 0.5 and lower than 1.0.

The classifications will be stored to disk in a three-column tab-delimited
text file, with the following columns:

1. Name of the BAM file that was classified.
2. Assigned category ("pos" or "neg" for positive and negative classifications,
   respectively, and "unknown" for the unknown category).
3. The probability of the assigned category.

E.g. an example output file could look like

::

    filename    predicted_class class_probability
    a.bam   neg 0.95
    b.bam   neg 0.88
    c.bam   pos 0.75
    d.bam   unknown 0.55


Examples
--------

Directory method, chrM, chunksize = 100, cores = 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    rna_cd-classify -m model.json -d bams_dir -j 3 -c chrM \
    --chunksize 100 -o classifications.out


List method, chrM, chunksize = 100, cores = 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    rna_cd-classify -m model.json -l bams.list -j 3 -c chrM \
    --chunksize 100 -o classifications.out


Usage
-----

.. click:: rna_cd.cli:classify_cli
    :prog: rna_cd-classify
    :show-nested:
