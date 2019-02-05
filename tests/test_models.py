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
import pytest
import magic

from unittest import mock
import numpy as np

import rna_cd.models


@pytest.fixture
def labels():
    # fake labels for mock array set
    return np.array(["pos"]*10 + ["neg"]*10)


def test_train_model(dataset, labels):
    positives, negatives = dataset
    with mock.patch("rna_cd.models.make_array_set") as mocked_array:
        # create array with shape (20, 500)
        mocked_array.return_value = (np.random.rand(20, 500), labels)
        result = rna_cd.models.train_svm_model(positive_bams=positives,
                                               negative_bams=negatives,
                                               chunksize=1000)
    assert mocked_array.call_count == 1
    steps = list(result.best_estimator_.named_steps.keys())
    assert sorted(steps) == sorted(["scale", "reduce_dim", "svm"])


def test_train_model_error():
    with pytest.raises(ValueError) as excinfo:
        rna_cd.models.train_svm_model([], [])
    assert str(excinfo.value) == ("The list of positive BAM files may not be "
                                  "empty.")


def test_train_model_error_negative(dataset):
    positives, _ = dataset
    with pytest.raises(ValueError) as excinfo:
        rna_cd.models.train_svm_model(positives, [])
    assert str(excinfo.value) == ("The list of negative BAM files may not be "
                                  "empty.")


def test_train_model_error_same_files(dataset):
    positives, _ = dataset
    with pytest.raises(ValueError) as excinfo:
        rna_cd.models.train_svm_model(positives, positives)
    assert str(excinfo.value) == ("Positive and negative BAM files may not be "
                                  "identical.")


def test_train_model_image(dataset, temp_path, labels):
    positives, negatives = dataset
    with mock.patch("rna_cd.models.make_array_set") as mocked_array:
        # create array with shape (20, 500)
        mocked_array.return_value = (np.random.rand(20, 500), labels)
        rna_cd.models.train_svm_model(positives, negatives, chunksize=1000,
                                      plot_out=temp_path)
    assert mocked_array.call_count == 1
    mimetype = magic.from_file(str(temp_path), mime=True)
    assert mimetype == "image/png"
