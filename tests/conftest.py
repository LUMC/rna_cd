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
from typing import List, Tuple
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path(__file__).parent / Path("data")


@pytest.fixture
def micro_bam(data_dir) -> Path:
    return data_dir / Path("micro.bam")


@pytest.fixture
def micro_bam2(data_dir) -> Path:
    return data_dir / Path("micro2.bam")


@pytest.fixture
def dataset(micro_bam, micro_bam2) -> Tuple[List[Path], List[Path]]:
    return [micro_bam]*10, [micro_bam2]*10


@pytest.fixture()
def temp_path() -> Path:
    tempf = NamedTemporaryFile(delete=False)
    path = Path(tempf.name)
    yield path
    path.unlink()  # removes it at teardown stage
