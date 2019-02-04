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
import datetime
from pathlib import Path
from typing import List, Any
import joblib
import click

import io
import base64
import json

import pkg_resources


def echo(msg: str):
    """Wrapper around click.secho to include datetime"""
    fmt = "[ {0} ] {1}".format(str(datetime.datetime.utcnow()), msg)
    click.secho(fmt, fg="green", err=True)


def load_list_file(path: Path) -> List[Path]:
    """Load a file containing containing a list of files"""
    with path.open("r") as handle:
        return [Path(x.strip()) for x in handle]


def dir_to_bam_list(path: Path) -> List[Path]:
    """Load a directory containing bam or cram files"""
    return [x for x in path.iterdir() if x.name.endswith(".bam")
            or x.name.endswith(".cram")]


def get_rna_cd_version():
    return pkg_resources.get_distribution("rna_cd").version


def get_sklearn_version():
    return pkg_resources.get_distribution("scikit-learn").version


def save_sklearn_object_to_disk(obj: Any, path: Path):
    """Save an object with some metadata to disk as serialized JSON"""
    b = io.BytesIO()
    d = {
        "rna_cd_version": get_rna_cd_version(),
        "sklearn_version": get_sklearn_version(),
        "datetime_stored": str(datetime.datetime.utcnow())
    }
    joblib.dump(obj, b, compress=True)
    dumped = b.getvalue()
    base64_encoded = base64.b64encode(dumped)
    d['obj'] = base64_encoded.decode('utf-8')
    with path.open("w") as handle:
        json.dump(d, handle)


def load_sklearn_object_from_disk(path: Path) -> Any:
    """Load a JSON-serialized object from disk"""
    with path.open("r") as handle:
        d = json.load(handle)
    if pkg_resources.parse_version(
            d.get("sklearn_version", "0.0.0")
    ) < pkg_resources.parse_version("0.20.0"):
        raise ValueError("We do not support loading objects with sklearn "
                         "versions below 0.20.0")
    blob = base64.b64decode(d.get("obj", ""))
    file_like_obj = io.BytesIO(blob)
    loaded = joblib.load(file_like_obj)
    return loaded
