"""
Copyright (C) 2018-2019  Leiden University Medical Center

This file is part of rna_cd

rna_cd is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

bam_process.py
~~~~~~~~~~~~~~

Process bam file to numpy array for classifications.
"""
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Iterator, Tuple, Callable, List, Any

import numpy as np
from pysam import AlignmentFile

from .utils import echo


def chop_contig(size: int, chunksize: int) -> Iterator[Tuple[int, int]]:
    """
    For a contig of given size, generate regions maximally chunksize long
    We use _0_ based indexing
    """

    if size < 1:
        raise ValueError("Size must be at least 1.")
    if chunksize < 1:
        raise ValueError("Chunksize must be at least 1.")

    pos = 0
    while pos < size:
        end = pos + chunksize
        if end < size:
            yield (pos, end)
        else:
            yield (pos, size)
        pos = end


def softclip_bases(reader: AlignmentFile, contig: str,
                   region: Tuple[int, int]) -> int:
    """Calculate amount of softclip bases for a region"""
    start, end = region
    it = reader.fetch(contig=contig, start=start, stop=end)
    s = 0
    for read in it:
        if read.cigartuples is not None:
            # cigartuples returns list of (operation, amount) tuple
            # where operation == 4 means softclip
            s += sum(amount for op, amount in read.cigartuples if op == 4)
    return s


def coverage(reader: AlignmentFile, contig: str, region: Tuple[int, int],
             method: Callable = np.mean) -> float:
    """Calculate average/median/etc coverage for a region"""
    start, end = region
    covs = reader.count_coverage(contig=contig, start=start, stop=end)

    return method(np.sum(covs, axis=0))


def process_bam(path: Path, chunksize: int = 100,
                contig: str = "chrM") -> np.ndarray:
    """
    Process bam file to an ndarray

    :returns: numpy ndarray of shape (n_features,)
    """
    echo("Calculating features for {0}".format(path.name))
    reader = AlignmentFile(str(path))
    try:
        contig_idx = reader.references.index(contig)
    except ValueError:
        raise ValueError("Contig {0} does not exist in BAM file".format(
            contig
        ))
    contig_size = reader.lengths[contig_idx]

    full_array = []
    tot_reads = 0
    for region in chop_contig(contig_size, chunksize):
        block = []
        start, end = region
        n_reads = reader.count(contig=contig, start=start, stop=end)
        tot_reads += n_reads
        cov = coverage(reader, contig, region)
        softclip = softclip_bases(reader, contig, region)
        block += [n_reads, cov, softclip]
        full_array += block
    # add normalization step
    normalized = np.array(full_array) / tot_reads
    echo("Done calculating features for {0}".format(path.name))
    return normalized


def make_array_set(bam_files: List[Path], labels: List[Any],
                   chunksize: int = 100,
                   contig: str = "chrM",
                   cores: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Make set of numpy arrays corresponding to data  and labels.
    I.e. train/testX and train/testY in scikit-learn parlance.

    :param bam_files: List of paths to bam files
    :param labels: list of labels.
    :param cores: number of cores to use for processing
    :return: tuple of X and Y numpy arrays. X has shape (n_files, n_features)
    Y has shape (n_files,).
    """
    if cores < 1:
        raise ValueError("Number of cores must be at least 1.")
    pool = Pool(cores)
    proc_func = partial(process_bam, chunksize=chunksize, contig=contig)
    # this returns a list of ndarrays.
    arr_X = pool.map(proc_func, bam_files)
    return np.array(arr_X), np.array(labels)
