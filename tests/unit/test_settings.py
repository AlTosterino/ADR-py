from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from adrpy.shared_kernel.errors import ConfigurationError
from adrpy.shared_kernel.settings import Settings

DIR_PATH = Path(__file__).parent
PYPROJECT_PATH = DIR_PATH / Path("pyproject.toml")
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
    with patch.object(Path, "cwd") as path_cwd_mock:
        path_cwd_mock.return_value = DIR_PATH
        settings = Settings()
        adr_dir = settings.adr_dir

    # When & Then
    assert adr_dir == DIR_PATH / Path("docs/adr")


def test_should_fallback_wrong_adr_dir_from_pyproject_toml_to_working_directory(
    wrong_pyproject_toml: None,
) -> None:
    # TODO: Maybe this shouldn't fallback, but raise instead?
    # Given
    with patch.object(Path, "cwd") as path_cwd_mock:
        path_cwd_mock.return_value = DIR_PATH
        settings = Settings()
        adr_dir = settings.adr_dir

    # When & Then
    assert adr_dir == DIR_PATH


def test_should_resolve_adr_dir_from_explicit_config_file(tmp_path: Path) -> None:
    config_path = tmp_path / ".adrpy.toml"
    config_path.write_text('dir = "docs/adr"')

    settings = Settings(config_path=config_path)

    assert settings.adr_dir == tmp_path / "docs/adr"


def test_should_resolve_adr_dir_from_explicitly_named_standalone_config(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "team-config.toml"
    config_path.write_text('dir = "docs/adr"')

    settings = Settings(config_path=config_path)

    assert settings.adr_dir == tmp_path / "docs/adr"


def test_should_raise_for_missing_explicit_config_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="does not exist"):
        Settings(config_path=tmp_path / ".adrpy.toml").adr_dir


def test_should_raise_for_malformed_explicit_config_file(tmp_path: Path) -> None:
    config_path = tmp_path / ".adrpy.toml"
    config_path.write_text("dir = [")

    with pytest.raises(ConfigurationError, match="Invalid TOML configuration"):
        Settings(config_path=config_path).adr_dir


def test_should_raise_for_invalid_adrpy_config_table(tmp_path: Path) -> None:
    config_path = tmp_path / "pyproject.toml"
    config_path.write_text("[tool.adrpy]\ndir = 42")

    with pytest.raises(ConfigurationError, match="non-empty string"):
        Settings(config_path=config_path).adr_dir
