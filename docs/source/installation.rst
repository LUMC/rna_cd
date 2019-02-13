Installation
============

``rna_cd`` is unfortunately not yet on PyPI. To install ``rna_cd``, acquire
the source code by cloning the git repository::

    $ git clone https://github.com/LUMC/rna_cd.git


Move to the rna_cd directory, and then install the package by running the
following in your python environment of choice::

    $ pip install '.'


This will install both the ``rna_cd`` python package, and install two
command line tools:

1. ``rna_cd-train``: For training a model using BAM files.
2. ``rna_cd-classify``: For classifying new BAM files.

Supported python versions
-------------------------

We only support the following python versions:

* python 3.5
* python 3.6
* python 3.7

Python 2 is **not** supported.
