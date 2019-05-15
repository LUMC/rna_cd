.. image:: https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)
    :target: http://bioconda.github.io/recipes/rna-cd/README.html
.. image:: https://travis-ci.org/LUMC/rna_cd.svg?branch=master
    :target: https://travis-ci.org/LUMC/rna_cd

.. image:: https://codecov.io/gh/LUMC/rna_cd/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/LUMC/rna_cd

.. image:: https://readthedocs.org/projects/rna-cd/badge/?version=latest
    :target: https://rna-cd.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

RNA Contamination Detector
==========================

rna_cd is a python package and command line tool designed to detect
RNA contamination of DNA-seq experiments.

For our complete documentation, please checkout our
`readthedocs page <https://rna-cd.readthedocs.io/en/latest/>`_.

Requirements
============

* Python 3.5+
* click
* scikit-learn
* pysam
* matplotlib


Installation
=============

PyPI
----

::

    $ pip install rna-cd

Conda
-----

::
    $ conda install -c bioconda rna-cd

License
=======

AGPLv3+