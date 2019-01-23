"""
rna_cd
Copyright (C) 2018-2019  Leiden University Medical Center, Sander Bollen

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
"""
import pytest

from rna_cd.bam_process import chop_contig


chop_contig_data = [
    ([1000, 100], [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500),
                   (500, 600), (600, 700), (700, 800), (800, 900),
                   (900, 1000)]),
    ([1000, 101], [(0, 101), (101, 202), (202, 303), (303, 404), (404, 505),
                   (505, 606), (606, 707), (707, 808), (808, 909),
                   (909, 1000)])
]


@pytest.mark.parametrize("args, expected", chop_contig_data)
def test_chop_contig(args, expected):
    assert list(chop_contig(*args)) == expected
