# Copyright (C) 2018-2019  Leiden University Medical Center
#
# This file is part of rna_cd
#
# rna_cd is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV

from .bam_process import make_array_set
from .utils import echo


def train_svm_model(positive_bams: List[Path], negative_bams: List[Path],
                    chunksize: int = 100, contig: str = "chrM",
                    cross_validations: int = 3, verbosity: int = 1,
                    cores: int = 1,
                    plot_out: Optional[Path] = None) -> GridSearchCV:
    """
    Run SVM training on a list of positive BAM files
    (i.e. _with_ contamination) and a list of negative BAM files
    (i.e. _without_ contamination).

    For all bam files features are collected over one contig. This contig is
    binned, and for each bin two different metrics of coverage are collected,
    in addition to the softclip rate.

    These features are then fed to a sklearn pipeline with three steps:

    1. A scaling step using StandardScaler
    2. A dimensional reduction step using PCA.
    3. A classification step using an SVM.

    Hyperparameters are tuned using a grid search with cross validations.

    Optionally saves a plot of the top two PCA components with the training
    samples.

    :param positive_bams: List of BAM files with contaminations
    :param negative_bams: List of BAM files without contaminations.
    :param chunksize: The size in bases for each chunk (bin)
    :param contig: The name of the contig.
    :param cross_validations: The amount of cross validations
    :param verbosity: Verbosity parameter of sklearn. Increase to see more
           messages.
    :param cores: Amount of cores to use for both metric collection and
           training.
    :param plot_out: Optional path for PCA plot.
    :returns: GridSearchCV object containing tuned pipeline.
    """
    if len(positive_bams) < 1:
        raise ValueError("The list of positive BAM files may not be empty.")
    if len(negative_bams) < 1:
        raise ValueError("The list of negative BAM files may not be empty.")

    # sets must be distjoint (i.e. no common elements)
    if not set(positive_bams).isdisjoint(set(negative_bams)):
        raise ValueError("An overlap exists between the lists of positive "
                         "and negative bam files.")
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
    components_params = list(range(2, max_components))
    param_grid = {
        "reduce_dim__n_components": components_params,
        "reduce_dim__whiten": [False, True],
        "svm__gamma": [0.1, 0.01, 0.001, 0.0001,
                       1, 10, 100, 1000],
        "svm__shrinking": [True, False],
        "svm__probability": [True]
    }
    pipeline = Pipeline(estimators)
    searcher = GridSearchCV(pipeline, cv=cross_validations,
                            param_grid=param_grid,
                            scoring="accuracy", verbose=verbosity,
                            pre_dispatch=1, n_jobs=cores)
    echo("Starting grid search for SVC model with {0} "
         "cross validations".format(cross_validations))
    searcher.fit(arr_X, arr_Y)
    echo("Finished gid search with best score: {0}.".format(
        searcher.best_score_)
    )
    echo("Best parameters: {0}".format(searcher.best_params_))

    if plot_out is not None:
        echo("Plotting training samples onto top 2 PCA components.")
        plot_pca(searcher, arr_X, arr_Y, plot_out)

    echo("Finished training.")
    return searcher


def plot_pca(searcher: GridSearchCV, arr_X: np.ndarray, arr_Y: np.ndarray,
             img_out: Path) -> None:
    """Plot PCA with training samples of pipeline."""

    pos_X = arr_X[arr_Y == "pos"]
    neg_X = arr_X[arr_Y == "neg"]

    best_pca = searcher.best_estimator_.named_steps['reduce_dim']
    pos_X_transformed = best_pca.transform(pos_X)
    neg_X_transformed = best_pca.transform(neg_X)

    fig = plt.figure(figsize=(6, 11))
    ax = fig.add_subplot(111)
    ax.scatter(pos_X_transformed[:, 0], pos_X_transformed[:, 1],
               color="red", label="Train positives")
    ax.scatter(neg_X_transformed[:, 0], neg_X_transformed[:, 1],
               color="blue", label="Train negatives")
    ax.set_xlabel("1st component")
    ax.set_ylabel("2nd component")
    ax.legend()
    fig.savefig(str(img_out), format="png", dpi=300)


def predict_labels_and_prob(model, bam_files: List[Path],
                            chunksize: int = 100, contig: str = "chrM",
                            cores: int = 1,
                            unknown_threshold: float = 0.75) -> Tuple[List[str], List[float]]:
    """
    Predict labels and probabilities for a list of bam files.

    :param unknown_threshold: The probability threshold below which samples
           are considered to be 'unknown'. Must be between 0.5 and 1.0

    :returns: tuple of List[predicted classes],
              List[probability for the most likely class]
    """
    if not 0.5 < unknown_threshold < 1.0:
        raise ValueError("unknown_threshold must be between 0.5 and 1.0")

    bam_arr, _ = make_array_set(bam_files, [], chunksize, contig, cores)
    prob = model.predict_proba(bam_arr)
    classes = []
    most_likely_prob = []
    for sample in prob:
        likely = max(sample)
        if likely < unknown_threshold:
            predicted_class = 'unknown'
        else:
            predicted_class = model.classes_[np.where(sample == likely)][0]
        classes.append(predicted_class)
        most_likely_prob.append(likely)
    return classes, most_likely_prob
