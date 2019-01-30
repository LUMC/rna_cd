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
from rna_cd.utils import (load_list_file, dir_to_bam_list,
                          save_sklearn_object_to_disk,
                          load_sklearn_object_from_disk)
from rna_cd import VERSION
import sklearn
import json
import pytest


def test_load_list_file(data_dir):
    listf = data_dir / Path("test_list.txt")
    loaded = load_list_file(listf)
    assert loaded == [
        Path("/path/to/bam1.bam"),
        Path("/path/to/bam2.bam"),
        Path("/path/to/bam3.bam"),
        Path("/path/to/bam4.bam"),
        Path("/path/to/bam5.bam"),
        Path("/path/to/bam6.bam"),
        Path("/path/to/bam7.bam"),
        Path("/path/to/bam8.bam"),
        Path("/path/to/bam9.bam")
    ]


def test_dir_to_bam_list(data_dir):
    bdir = data_dir / Path("test_bam_cram")
    loaded = dir_to_bam_list(bdir)
    exp = ([bdir / Path("{0}.bam".format(x)) for x in range(1, 11)] +
           [bdir / Path("{0}.cram".format(x)) for x in range(1, 11)])
    assert sorted(loaded) == sorted(exp)


def test_save_to_disk(temp_path):
    an_obj = "some_string"
    save_sklearn_object_to_disk(an_obj, temp_path)
    assert temp_path.exists()
    with temp_path.open("r") as handle:
        j = json.load(handle)
    assert j['rna_cd_version'] == str(VERSION)
    assert j['sklearn_version'] == sklearn.__version__


def test_load_valid(data_dir):
    valid_path = data_dir / Path("valid_obj.json")
    obj = load_sklearn_object_from_disk(valid_path)
    assert obj == "some_string"


def test_load_invalid(data_dir):
    invalid_path = data_dir / Path("invalid_obj.json")
    with pytest.raises(ValueError) as exp:
        load_sklearn_object_from_disk(invalid_path)
    assert exp.match("We do not support loading objects with sklearn versions "
                     "below 0.20.0")
