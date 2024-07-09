from pathlib import Path
from typing import Generator

import pytest
from adrpy.shared_kernel.settings import Settings

PYPROJECT_PATH = Path("pyproject.toml")
PYPROJECT_DATA = """
    [tool.adrpy]
    dir = "docs/adr"
    """
PYPROJECT_WRONG_DATA = """
    [tool.adrpython]
    dir = "docs/adr"
    """


@pytest.fixture(scope="module")
def correct_pyproject_toml() -> Generator[None, None, None]:
    with open(PYPROJECT_PATH, "w") as pyproject:
        pyproject.write(PYPROJECT_DATA)
    yield
    Path(PYPROJECT_PATH).unlink(missing_ok=True)


@pytest.fixture(scope="module")
def wrong_pyproject_toml() -> Generator[None, None, None]:
    with open(PYPROJECT_PATH, "w") as pyproject:
        pyproject.write(PYPROJECT_WRONG_DATA)
    yield
    Path(PYPROJECT_PATH).unlink(missing_ok=True)


def test_should_get_adr_dir_from_settings_when_no_initial_dir_set() -> None:
    # Given
    settings = Settings()

    # When & Then
    assert Path.cwd() == settings.adr_dir


def test_should_get_adr_dir_from_settings_when_initial_dir_set() -> None:
    # Given
    settings = Settings(initial_adr_dir=Path(__file__).parent)

    # When & Then
    assert settings.adr_dir == Path(__file__).parent


def test_should_get_adr_dir_from_pyproject_toml(correct_pyproject_toml: None) -> None:
    # Given
    settings = Settings()

    # When & Then
    assert settings.adr_dir == Path.cwd() / Path("docs/adr")


def test_should_fallback_wrong_adr_dir_from_pyproject_toml_to_working_directory(
    wrong_pyproject_toml: None,
) -> None:
    # TODO: Maybe this shouldn't fallback, but raise instead?
    # Given
    settings = Settings()

    # When & Then
    assert settings.adr_dir == Path.cwd()
