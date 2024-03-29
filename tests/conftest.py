import shutil
from typing import Iterator

import pytest
from adrpy.injection import setup_injection
from lidipy import Lidi

from tests.fixtures.repository import TEST_DIRECTORY

pytest_plugins = ["tests.fixtures"]


@pytest.fixture
def lidi() -> Lidi:
    from adrpy.injection import lidi

    setup_injection()
    yield lidi


@pytest.fixture(autouse=True)
def remove_test_file() -> Iterator[None]:
    yield
    shutil.rmtree(TEST_DIRECTORY, ignore_errors=True)
