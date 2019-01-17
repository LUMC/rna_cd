"""
rna_cd
Copyright (C) 2018-2019  Leiden University Medical Center, Sander Bollen

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
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path(__file__).parent / Path("data")


@pytest.fixture()
def temp_path() -> Path:
    tempf = NamedTemporaryFile(delete=False)
    path = Path(tempf.name)
    yield path
    path.unlink()  # removes it at teardown stage
