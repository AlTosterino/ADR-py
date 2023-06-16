import pytest
from adrpy.injection import setup_injection
from lidipy import Lidi


@pytest.fixture
def lidi() -> Lidi:
    from adrpy.injection import lidi

    setup_injection()
    yield lidi
