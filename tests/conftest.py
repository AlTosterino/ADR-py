from typing import cast

import pytest
from injector import Injector


@pytest.fixture
def injector() -> Injector:
    from adrpy.injection import injector

    return cast(Injector, injector)
