from pathlib import Path
from typing import Iterator

import pytest
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.repositories.adr.repository import ADRFileRepository
from adrpy.shared_kernel.settings import Settings
from lidipy import Lidi

TEST_DIRECTORY = Path(__file__).parent / "testdir"
TEST_FILENAME = "testfile"
TEST_FILENAME_WITH_EXTENSION = "testfile.md"


@pytest.fixture()
def repo_service(lidi: Lidi) -> Iterator[BaseADRRepository]:
    original_repo = lidi.resolve(BaseADRRepository)
    original_settings = lidi.resolve(Settings)
    new_settings = Settings(initial_adr_dir=TEST_DIRECTORY)
    lidi.bind(BaseADRRepository, ADRFileRepository(settings=new_settings))
    yield lidi.resolve(BaseADRRepository)
    lidi.bind(BaseADRRepository, original_repo)
    lidi.bind(Settings, original_settings)
