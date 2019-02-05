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

from rna_cd.models import train_svm_model


def test_train_model(dataset):
    positives, negatives = dataset
    result = train_svm_model(positive_bams=positives, negative_bams=negatives,
                             chunksize=1000)
    steps = list(result.best_estimator_.named_steps.keys())
    assert sorted(steps) == sorted(["scale", "reduce_dim", "svm"])


def test_train_model_error():
    with pytest.raises(ValueError) as excinfo:
        train_svm_model([], [])
    assert str(excinfo.value) == ("The list of positive BAM files may not be "
                                  "empty.")


def test_train_model_error_negative(dataset):
    positives, _ = dataset
    with pytest.raises(ValueError) as excinfo:
        train_svm_model(positives, [])
    assert str(excinfo.value) == ("The list of negative BAM files may not be "
                                  "empty.")


def test_train_model_error_same_files(dataset):
    positives, _ = dataset
    with pytest.raises(ValueError) as excinfo:
        train_svm_model(positives, positives)
    assert str(excinfo.value) == ("Positive and negative BAM files may not be "
                                  "identical.")


def test_train_model_image(dataset, temp_path):
    positives, negatives = dataset
    train_svm_model(positives, negatives, chunksize=1000, plot_out=temp_path)
    mimetype = magic.from_file(str(temp_path), mime=True)
    assert mimetype == "image/png"
