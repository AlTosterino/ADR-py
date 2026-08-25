import shutil
from typing import Generator, Iterator

import pytest
from lidipy import Lidi

from adrpy.injection import lidi as injection_lidi
from adrpy.injection import setup_injection
from tests.fixtures.repository import TEST_DIRECTORY

pytest_plugins = ["fixtures.repository"]


@pytest.fixture
def lidi() -> Generator[Lidi, None, None]:
    setup_injection()
    yield injection_lidi


@pytest.fixture(autouse=True)
def remove_test_files() -> Iterator[None]:
    yield
    shutil.rmtree(TEST_DIRECTORY, ignore_errors=True)
