import shutil
from typing import Iterator

import pytest
from lidipy import Lidi

from adrpy.injection import setup_injection
from tests.fixtures.repository import TEST_DIRECTORY

pytest_plugins = ["fixtures.repository"]


@pytest.fixture
def lidi() -> Lidi:
    from adrpy.injection import lidi

    setup_injection()
    yield lidi


@pytest.fixture(autouse=True)
def remove_test_files() -> Iterator[None]:
    yield
    shutil.rmtree(TEST_DIRECTORY, ignore_errors=True)
