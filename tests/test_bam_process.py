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
"""
from pathlib import Path
from pysam import AlignmentFile
import pytest

from rna_cd.bam_process import (chop_contig, coverage, softclip_bases,
                                process_bam, make_array_set)


chop_contig_data = [
    ([1000, 100], [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500),
                   (500, 600), (600, 700), (700, 800), (800, 900),
                   (900, 1000)]),
    ([1000, 101], [(0, 101), (101, 202), (202, 303), (303, 404), (404, 505),
                   (505, 606), (606, 707), (707, 808), (808, 909),
                   (909, 1000)])
]


fail_contig_data = [
    ((0, 100), ValueError("Size must be at least 1.")),
    ((100, 0), ValueError("Chunksize must be at least 1."))
]


make_array_set_cores = list(range(1, 10))


@pytest.fixture
def micro_bam(data_dir):
    return data_dir / Path("micro.bam")


@pytest.mark.parametrize("args, expected", chop_contig_data)
def test_chop_contig(args, expected):
    assert list(chop_contig(*args)) == expected


@pytest.mark.parametrize("args, expected", fail_contig_data)
def test_fail_chop_contig(args, expected):
    with pytest.raises(type(expected)) as excinfo:
        chopper = chop_contig(*args)
        next(chopper)
    assert str(excinfo.value) == str(expected)


def test_coverage(micro_bam):
    alignment_file = AlignmentFile(str(micro_bam))
    assert int(coverage(alignment_file, 'chrM', (1000, 2000))) == 123


def test_softclip(micro_bam):
    alignment_file = AlignmentFile(str(micro_bam))
    assert softclip_bases(alignment_file, 'chrM', (1000, 2000)) == 96


def test_process_bam_len(micro_bam):
    returned = process_bam(micro_bam, 16571)  # one chunk
    assert len(returned) == 3


def test_process_bam_contents(micro_bam):
    returned = process_bam(micro_bam, 16571)  # one chunk
    assert returned[0] == 1
    assert 0.007 < returned[1] < 0.008  # it's a float
    assert 0.56 < returned[2] < 0.57  # it's a float


@pytest.mark.parametrize("cores", make_array_set_cores)
def test_make_array_set(cores, micro_bam):
    path_set = [micro_bam]*10
    labels = ["pos"]*10
    data_array, returned_labels = make_array_set(path_set, labels,
                                                 cores=cores, chunksize=1000)
    assert data_array.shape == (10, 51)


def test_make_array_set_error(micro_bam):
    with pytest.raises(ValueError) as excinfo:
        make_array_set([micro_bam], ["pos"], cores=0)
    assert str(excinfo.value) == "Number of cores must be at least 1."
