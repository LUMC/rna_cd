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
from click.testing import CliRunner
from click import BadParameter
from collections import namedtuple
from pathlib import Path
from unittest import mock
from tempfile import NamedTemporaryFile

import pytest
import numpy as np

from rna_cd.cli import (directory_callback, list_callback, path_callback,
                        train_cli, classify_cli)

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


train_cli_errors_data = [
    (["-o", "some_random_path"],
     ValueError("Must set either --positives-dir or --positives-list")),
    (["-o", "some_random_path", "-pl", str(_listf)],
     ValueError("Must set either --negatives-dir or --negatives-list"))
]


classify_cli_errors_data = [
    (["-m", str(_listf), "-o", "someething"],
     ValueError("Must set either --directory or --list-items"))
]


@pytest.fixture
def make_dataset_lists(dataset):
    positives, negatives = dataset
    pos_list_f = Path(NamedTemporaryFile(delete=False).name)
    neg_list_f = Path(NamedTemporaryFile(delete=False).name)

    with pos_list_f.open("w") as pos_handle:
        for pos in positives:
            pos_handle.write(str(pos)+"\n")

    with neg_list_f.open("w") as neg_handle:
        for neg in negatives:
            neg_handle.write(str(neg)+"\n")

    yield pos_list_f, neg_list_f

    # teardown
    pos_list_f.unlink()
    neg_list_f.unlink()


@pytest.fixture
def labels():
    # fake labels for mock array set
    return np.array(["pos"]*10 + ["neg"]*10)


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


@pytest.mark.parametrize("args, expected", train_cli_errors_data)
def test_train_cli_errors(args, expected):
    runner = CliRunner()
    result = runner.invoke(train_cli, args)
    assert result.exit_code != 0
    assert type(result.exception) == type(expected)
    assert result.exception.args[0] == expected.args[0]


@pytest.mark.parametrize("args, expected", classify_cli_errors_data)
def test_classify_cli_errors(args, expected):
    runner = CliRunner()
    result = runner.invoke(classify_cli, args)
    assert result.exit_code != 0
    assert type(result.exception) == type(expected)
    assert result.exception.args[0] == expected.args[0]


def test_train_cli(make_dataset_lists, temp_path, labels):
    pos_list, neg_list = make_dataset_lists
    runner = CliRunner()
    args = ["-pl", str(pos_list), "-nl", str(neg_list), "-o", str(temp_path),
            "--chunksize", 1000]
    with mock.patch("rna_cd.models.make_array_set") as mocked_array:
        # create array with shape (20, 500)
        mocked_array.return_value = (np.random.rand(20, 500), labels)
        result = runner.invoke(train_cli, args)
    mocked_array.assert_called_once()
    assert result.exit_code == 0
    assert "Finished training." in result.output
