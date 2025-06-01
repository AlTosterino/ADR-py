import dataclasses
from pathlib import Path
from typing import Iterator

import pytest
from lidipy import Lidi

from adrpy.repositories.adr.base import IADRRepository
from adrpy.repositories.adr.repository import ADRFileRepository
from adrpy.shared_kernel.settings import Settings

TEST_DIRECTORY = Path(__file__).parent / "testdir"
TEST_FILENAME = "0001-testfile"
TEST_FILENAME_WITH_EXTENSION = "0001-testfile.md"


@pytest.fixture()
def adr_repository(lidi: Lidi) -> Iterator[IADRRepository]:
    original_repo = lidi.resolve(IADRRepository)
    original_settings = lidi.resolve(Settings)
    lidi.bind(Settings, dataclasses.replace(original_settings, initial_adr_dir=TEST_DIRECTORY))
    lidi.bind(IADRRepository, ADRFileRepository)
    yield lidi.resolve(IADRRepository)
    lidi.bind(IADRRepository, original_repo)
    lidi.bind(Settings, original_settings)
