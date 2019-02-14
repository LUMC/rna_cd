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
import click
from pathlib import Path
from typing import Optional, List

from .models import train_svm_model, predict_labels_and_prob
from .utils import (load_list_file, dir_to_bam_list,
                    save_sklearn_object_to_disk,
                    load_sklearn_object_from_disk, echo)


# all callback functions but adhere to the following signature:
# def callback(ctx, param, value)
# See https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options  # noqa
def directory_callback(ctx, param, value):
    """Click callback function for getting bam/cram files from a directory."""
    if value is None:
        return None

    if param.name == "positives_dir" and "positives_list" in ctx.params:
        raise click.BadParameter("--positives-dir and --positives-list "
                                 "are mutually exclusive.")
    elif param.name == "negatives_dir" and "negatives_list" in ctx.params:
        raise click.BadParameter("--negatives-dir and --negatives-list "
                                 "are mutually exclusive.")
    return dir_to_bam_list(Path(value))


def list_callback(ctx, param, value):
    """Click callback function for getting bam/cram files from a list file."""
    if value is None:
        return None

    if param.name == "positives_list" and "positives_dir" in ctx.params:
        raise click.BadParameter("--positives-list and --positives-dir "
                                 "are mutually exclusive.")
    elif param.name == "negatives_list" and "negatives_dir" in ctx.params:
        raise click.BadParameter("--negatives-list and --negatives-dir "
                                 "are mutually exclusive.")
    return load_list_file(Path(value))


def path_callback(ctx, param, value):
    """
    Generic str to path callback.
    To be used for click.Path types that ought to return pathlib.Path
    """
    if value is None:
        return None
    return Path(value)


def unknown_threshold_callback(ctx, param, value):
    """
    Click callback function for threshold that has to be between 0.5 and 1.0
    """
    if not 0.5 < value < 1.0:
        raise click.BadParameter("value must be between 0.5 "
                                 "and 1.0")
    return value


@click.command()
@click.option("--chunksize", type=click.INT, default=100,
              help="Chunksize in bases. Default = 100")
@click.option("-c", "--contig", type=click.STRING, default="chrM",
              help="Name of mitochrondrial contig in your BAM files. "
                   "Default = chrM")
@click.option("-pd", "--positives-dir",
              type=click.Path(exists=True, dir_okay=True,
                              file_okay=False, readable=True),
              callback=directory_callback,
              help="Path to directory containing positive BAM files. "
                   "Mutually exclusive with --positives-list")
@click.option("-nd", "--negatives-dir",
              type=click.Path(exists=True, dir_okay=True,
                              file_okay=False, readable=True),
              callback=directory_callback,
              help="Path to directory containing negative BAM files. "
                   "Mutually exlusive with --negatives-list")
@click.option("-pl", "--positives-list",
              type=click.Path(exists=True, dir_okay=False,
                              file_okay=True, readable=True),
              callback=list_callback,
              help="Path to file containing a list of paths to positive BAM "
                   "files. Mutually exclusive with --positives-dir")
@click.option("-nl", "--negatives-list",
              type=click.Path(exists=True, dir_okay=False,
                              file_okay=True, readable=True),
              callback=list_callback,
              help="Path to file containing a list of paths to negative BAM "
                   "files. Mutuallly exclusive with --negatives-dir")
@click.option("--cross-validations", type=click.INT, default=3,
              help="Number of folds for cross validation run. Default = 3")
@click.option("--verbosity", type=click.INT, default=1,
              help="Verbosity value for cross validation step. Default = 1")
@click.option("-j", "--cores", type=click.INT, default=1,
              help="Number of cores to use for processing of BAM files "
                   "and cross validations. Default = 1")
@click.option("--plot-out", type=click.Path(writable=True),
              help="Optional path to PCA plot.")
@click.option("-o", "--model-out", type=click.Path(writable=True),
              required=True,
              help="Path where model will be stored.")
def train_cli(chunksize: int, contig: str, model_out: Path,
              positives_dir: Optional[List[Path]] = None,
              negatives_dir: Optional[List[Path]] = None,
              positives_list: Optional[List[Path]] = None,
              negatives_list: Optional[List[Path]] = None,
              cross_validations: int = 3,
              verbosity: int = 1, cores: int = 1,
              plot_out: Optional[str] = None):

    if positives_dir is None and positives_list is None:
        raise ValueError("Must set either --positives-dir or --positives-list")

    if negatives_dir is None and negatives_list is None:
        raise ValueError("Must set either --negatives-dir or --negatives-list")

    positives = positives_dir if positives_dir is not None else positives_list
    negatives = negatives_dir if negatives_dir is not None else negatives_list

    model = train_svm_model(positives, negatives, chunksize=chunksize,
                            contig=contig, cross_validations=cross_validations,
                            verbosity=verbosity, cores=cores,
                            plot_out=plot_out)

    save_sklearn_object_to_disk(model, Path(model_out))


@click.command()
@click.option("--chunksize", type=click.INT, default=100,
              help="Chunksize in bases. Default = 100")
@click.option("-c", "--contig", type=click.STRING, default="chrM",
              help="Name of mitochrondrial contig in your BAM files. "
                   "Default = chrM")
@click.option("-j", "--cores", type=click.INT, default=1,
              help="Number of cores to use for processing of BAM files. "
                   "Default = 1")
@click.option("-d", "--directory",
              type=click.Path(exists=True, readable=True,
                              dir_okay=True, file_okay=False),
              callback=directory_callback,
              help="Path to directory with BAM files to be tested. "
                   "Mutually exclusive with --list-items")
@click.option("-l", "--list-items",
              type=click.Path(exists=True, readable=True,
                              file_okay=True, dir_okay=False),
              callback=list_callback,
              help="Path to file containing list of paths to BAM files to be "
                   "tested. Mutually exclusive with --directory")
@click.option("-m", "--model",
              type=click.Path(exists=True, readable=True,
                              file_okay=True, dir_okay=False),
              callback=path_callback, required=True,
              help="Path to model."
              )
@click.option("-o", "--output", type=click.Path(writable=True),
              required=True, callback=path_callback,
              help="Path to output file containing classifications.")
@click.option("-t", "--unknown-threshold", type=click.FLOAT, default=0.75,
              help="Threshold of most likely probability below which samples"
                   "wll be assinged as 'unknown'. Default = 0.75",
              callback=unknown_threshold_callback)
def classify_cli(chunksize: int, contig: str, cores: int,
                 directory: Optional[List[Path]],
                 list_items: Optional[List[Path]], model: Path,
                 output: Path, unknown_threshold: float):

    if directory is None and list_items is None:
        raise ValueError("Must set either --directory or --list-items")

    bam_files = directory if directory is not None else list_items

    echo("Loading model from disk.")
    sklearn_model = load_sklearn_object_from_disk(model)
    echo("Running predictions.")
    predicted_classes, probabilities = predict_labels_and_prob(
        sklearn_model, bam_files, chunksize=chunksize,
        contig=contig, cores=cores, unknown_threshold=unknown_threshold)
    echo("Writing predictions to disk.")
    with output.open("w") as ohandle:
        header = 'filename\tpredicted_class\tclass_probability\n'
        ohandle.write(header)
        for i, bam in enumerate(bam_files):
            fmt = "{fname}\t{cl}\t{prob}\n".format(
                fname=bam.name,
                cl=predicted_classes[i],
                prob=probabilities[i]
            )
            ohandle.write(fmt)
    echo("Done.")
