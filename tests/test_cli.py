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
from click.testing import CliRunner
from click import BadParameter
from collections import namedtuple
from pathlib import Path

import pytest

from rna_cd.cli import directory_callback, list_callback, path_callback

MockParam = namedtuple("MockParam", ["name"])
MockCtx = namedtuple("MockCtx", ["params"])


# cannot use a fixture here because pytest hairiness around parametrizations.
# see https://github.com/pytest-dev/pytest/issues/349
_listf = Path(__file__).parent / Path("data") / Path("test_list.txt")
_bamf = Path(__file__).parent / Path("data") / Path("test_bam_cram")


dir_callback_data = [
    ([None, None, None], None),
    ([MockCtx(["positives_list"]), MockParam("positives_dir"), ""],
     BadParameter('')),
    ([MockCtx(["negatives_list"]), MockParam("negatives_dir"), ""],
     BadParameter('')),
    ([MockCtx([]), MockParam("positives_dir"), str(_bamf)], [
        Path(_bamf) / Path("1.bam"), Path(_bamf) / Path("1.cram"),
        Path(_bamf) / Path("2.bam"), Path(_bamf) / Path("2.cram"),
        Path(_bamf) / Path("3.bam"), Path(_bamf) / Path("3.cram"),
        Path(_bamf) / Path("4.bam"), Path(_bamf) / Path("4.cram"),
        Path(_bamf) / Path("5.bam"), Path(_bamf) / Path("5.cram"),
        Path(_bamf) / Path("6.bam"), Path(_bamf) / Path("6.cram"),
        Path(_bamf) / Path("7.bam"), Path(_bamf) / Path("7.cram"),
        Path(_bamf) / Path("8.bam"), Path(_bamf) / Path("8.cram"),
        Path(_bamf) / Path("9.bam"), Path(_bamf) / Path("9.cram"),
        Path(_bamf) / Path("10.bam"), Path(_bamf) / Path("10.cram")
    ]),
    ([MockCtx([]), MockParam("negatives_dir"), str(_bamf)], [
        Path(_bamf) / Path("1.bam"), Path(_bamf) / Path("1.cram"),
        Path(_bamf) / Path("2.bam"), Path(_bamf) / Path("2.cram"),
        Path(_bamf) / Path("3.bam"), Path(_bamf) / Path("3.cram"),
        Path(_bamf) / Path("4.bam"), Path(_bamf) / Path("4.cram"),
        Path(_bamf) / Path("5.bam"), Path(_bamf) / Path("5.cram"),
        Path(_bamf) / Path("6.bam"), Path(_bamf) / Path("6.cram"),
        Path(_bamf) / Path("7.bam"), Path(_bamf) / Path("7.cram"),
        Path(_bamf) / Path("8.bam"), Path(_bamf) / Path("8.cram"),
        Path(_bamf) / Path("9.bam"), Path(_bamf) / Path("9.cram"),
        Path(_bamf) / Path("10.bam"), Path(_bamf) / Path("10.cram")
    ])
]


list_callback_data = [
    ([None, None, None], None),
    ([MockCtx(["positives_dir"]), MockParam("positives_list"), ""],
     BadParameter("")),
    ([MockCtx(["negatives_dir"]), MockParam("negatives_list"), ""],
     BadParameter("")),
    ([MockCtx([]), MockParam("positives_list"), str(_listf)], [
        Path("/path/to/bam1.bam"), Path("/path/to/bam2.bam"),
        Path("/path/to/bam3.bam"), Path("/path/to/bam4.bam"),
        Path("/path/to/bam5.bam"), Path("/path/to/bam6.bam"),
        Path("/path/to/bam7.bam"), Path("/path/to/bam8.bam"),
        Path("/path/to/bam9.bam")
    ]),
    ([MockCtx([]), MockParam("negatives_list"), str(_listf)], [
        Path("/path/to/bam1.bam"), Path("/path/to/bam2.bam"),
        Path("/path/to/bam3.bam"), Path("/path/to/bam4.bam"),
        Path("/path/to/bam5.bam"), Path("/path/to/bam6.bam"),
        Path("/path/to/bam7.bam"), Path("/path/to/bam8.bam"),
        Path("/path/to/bam9.bam")
    ])
]


path_callback_data = [
    (None, None),
    ("something", Path("something"))
]


@pytest.mark.parametrize("args, expected", dir_callback_data)
def test_dir_callback(args, expected):
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            directory_callback(*args)
    elif expected is not None:
        assert sorted(directory_callback(*args)) == sorted(expected)
    else:
        assert directory_callback(*args) == expected


@pytest.mark.parametrize("args, expected", list_callback_data)
def test_list_callback(args, expected):
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            list_callback(*args)
    else:
        assert list_callback(*args) == expected


@pytest.mark.parametrize("value, expected", path_callback_data)
def test_path_callback(value, expected):
    assert path_callback(None, None, value) == expected
