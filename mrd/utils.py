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
import datetime
from pathlib import Path
from typing import List, NamedTuple, Any
import joblib
import click
import sklearn


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int

    def __str__(self):
        return "{0}.{1}.{2}".format(
            self.major, self.minor, self.patch
        )


VERSION = VersionInfo(0, 0, 1)


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


def save_sklearn_object_to_disk(obj: Any, path: Path):
    """Save an object with some metadata to disk"""
    d = {
        "mrd_version": str(VERSION),
        "sklearn_version": sklearn.__version__,
        "datetime_stored": str(datetime.datetime.utcnow()),
        "object": obj
    }
    joblib.dump(d, str(path))
