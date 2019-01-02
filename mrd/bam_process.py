"""
mrd
Copyright (C) 2018  Leiden University Medical Center, Sander Bollen

This program is free software: you can redistribute it and/or modify
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
    it = reader.fetch(contig=contig, start=region[0], stop=region[1])
    s = 0
    for read in it:
        if read.cigartuples is not None:
            s += sum(amount for op, amount in read.cigartuples if op == 4)
    return s


def coverage(reader: AlignmentFile, contig: str, region: Tuple[int, int],
             method: Callable = np.mean) -> int:
    """Calculate average/median/etc coverage for a region"""
    covs = reader.count_coverage(contig=contig, start=region[0],
                                 stop=region[1])

    return method(np.sum(covs))


def process_bam(path: Path, chunksize: int = 100,
                contig: str = "chrM") -> np.ndarray:
    """Process bam file to an ndarray"""
    echo("Calculating features for {0}".format(path.name))
    reader = AlignmentFile(str(path))
    try:
        ctg_idx = reader.references.index(contig)
    except ValueError:
        raise ValueError("Contig {0} does not exist in BAM file".format(
            contig
        ))
    contig_size = reader.lengths[ctg_idx]

    arr = []
    for region in chop_contig(contig_size, chunksize):
        block = []
        n_reads = reader.count(contig=contig, start=region[0], stop=region[1])
        cov = coverage(reader, contig, region)
        softclip = softclip_bases(reader, contig, region)
        block += [n_reads, cov, softclip]
        arr += block
    echo("Done calculating features for {0}".format(path.name))
    return np.array(arr)


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
    :return: tuple of X and Y numpy arrays. X = 2d, Y = 1d
    """
    pool = Pool(cores)
    proc_func = partial(process_bam, chunksize=chunksize, contig=contig)
    arr_X = pool.map(proc_func, bam_files)
    return np.array(arr_X), np.array(labels)
