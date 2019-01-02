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
"""
from pathlib import Path
from typing import List

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, OneClassSVM
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix

from .bam_process import make_array_set
from .utils import echo


def train_svm_model(positive_bams: List[Path], negative_bams: List[Path],
                    chunksize: int = 100, contig: str = "chrM",
                    cross_validations: int = 3, verbosity: int = 1,
                    cores: int = 1):
    labels = ["pos"]*len(positive_bams) + ["neg"]*len(negative_bams)
    arr_X, arr_Y = make_array_set(positive_bams+negative_bams, labels,
                                  chunksize, contig, cores)
    estimators = [
        ("scale", StandardScaler()),
        ("reduce_dim", PCA()),
        ("svm", SVC())
    ]
    echo("Setting up processing pipeline for SVM model")

    # components MUST fall between 0 ... min(n_samples, n_features)
    # cross-validation additionally reduces amount of samples
    n_samples = int(arr_X.shape[0] * (1 - (1/cross_validations)))
    max_components = min(n_samples, arr_X.shape[1])
    components_params = list(range(1, max_components+1, 10))
    param_grid = {
        "reduce_dim__n_components": components_params,
        "reduce_dim__whiten": [False, True],
        "svm__gamma": [0.1, 0.01, 0.001, 0.0001,
                       1, 10, 100, 1000],
        "svm__shrinking": [True, False]
    }
    pipeline = Pipeline(estimators)
    searcher = GridSearchCV(pipeline, cv=cross_validations,
                            param_grid=param_grid,
                            scoring="accuracy", verbose=verbosity,
                            n_jobs=cores)
    echo("Starting grid search for SVC model with {0} "
         "cross validations".format(cross_validations))
    searcher.fit(arr_X, arr_Y)
    echo(searcher.best_params_)

    # evaluating on train set = BAD!
    pred_Y = searcher.predict(arr_X)
    confused = confusion_matrix(arr_Y, pred_Y)
    echo(confused)
