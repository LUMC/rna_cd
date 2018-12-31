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

from .bam_process import process_bam
from .utils import echo


def train_svm_model(positive_bams: List[Path], negative_bams: List[Path],
                    chunksize: int = 100, contig: str = "chrM",
                    cross_validations: int = 3, verbosity: int = 1):
    arr = []
    for bam in positive_bams + negative_bams:
        echo("Calculating features for {0}".format(bam.name))
        arr.append(process_bam(bam, chunksize, contig))
        echo("Done calculating features for {0}".format(bam.name))
    arr = np.array(arr)
    Y = np.array(["pos"]*len(positive_bams) + ["neg"]*len(negative_bams))
    estimators = [
        ("scale", StandardScaler()),
        ("reduce_dim", PCA()),
        ("svm", SVC())
    ]
    echo("Setting up processing pipeline for SVM model")

    # components MUST fall between 0 ... min(n_samples, n_features)
    # cross-validation additionally reduces amount of samples
    n_samples = int((len(arr) * (1 - (1/cross_validations))))
    max_components = min(n_samples, len(arr[0]))
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
                            scoring="accuracy", verbose=verbosity)
    echo("Starting grid search for SVC model with {0} "
         "cross validations".format(cross_validations))
    searcher.fit(arr, Y)
    echo(searcher.cv_results_)
