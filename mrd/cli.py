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
import click
from pathlib import Path
from typing import Optional, List

from .models import train_svm_model
from .utils import load_list_file, dir_to_bam_list


def directory_callback(ctx, param, value):
    if value is None:
        return None

    if param == "positives_dir" and "positives_list" in ctx.params:
        raise ValueError("--positives-dir and --positives-list "
                         "are mutually exclusive.")
    elif param == "negatives_dir" and "negatives_list" in ctx.params:
        raise ValueError("--negatives-dir and --negatives-list "
                         "are mutually exclusive.")
    return dir_to_bam_list(Path(value))


def list_callback(ctx, param, value):
    if value is None:
        return None

    if param == "positives_list" and "positives_dir" in ctx.params:
        raise ValueError("--positives-list and --positives-dir "
                         "are mutually exclusive.")
    elif param == "negatives_list" and "negatives_dir" in ctx.params:
        raise ValueError("--negatives-list and --negatives-dir "
                         "are mutually exclusive.")
    return load_list_file(Path(value))


@click.command()
@click.option("--chunksize", type=click.INT, default=100)
@click.option("-c", "--contig", type=click.STRING, default="chrM")
@click.option("-pd", "--positives-dir",
              type=click.Path(exists=True, dir_okay=True,
                              file_okay=False, readable=True),
              callback=directory_callback)
@click.option("-nd", "--negatives-dir",
              type=click.Path(exists=True, dir_okay=True,
                              file_okay=False, readable=True),
              callback=directory_callback)
@click.option("-pl", "--positives-list",
              type=click.Path(exists=True, dir_okay=False,
                              file_okay=True, readable=True),
              callback=list_callback)
@click.option("-nl", "--negatives-list",
              type=click.Path(exists=True, dir_okay=False,
                              file_okay=True, readable=True),
              callback=list_callback)
def train_cli(chunksize: int, contig: str,
              positives_dir: Optional[List[Path]] = None,
              negatives_dir: Optional[List[Path]] = None,
              positives_list: Optional[List[Path]] = None,
              negatives_list: Optional[List[Path]] = None):

    positives = positives_dir if positives_dir is not None else positives_list
    negatives = negatives_dir if negatives_dir is not None else negatives_list

    train_svm_model(positives, negatives, chunksize=chunksize, contig=contig)
