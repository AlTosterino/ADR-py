from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import cast

from adrpy.shared_kernel.errors import ConfigurationError


@dataclass(frozen=True)
class Settings:
    # TODO: Add DEBUG logger handler
    initial_adr_dir: Path | None = None  # TODO: Rename to requested_adr_dir or something
    config_path: Path | None = None
    APP_TEMPLATES_DIR: Path = field(init=False, default=Path(__file__).parents[1] / "templates")

    @cached_property
    def adr_dir(self) -> Path:
        if self.initial_adr_dir:
            return self.initial_adr_dir
        if adr_dir_from_config := self.__get_adr_dir_from_config():
            return adr_dir_from_config
        return self.working_directory

    @cached_property
    def working_directory(self) -> Path:
        return Path.cwd()

    def __get_adr_dir_from_config(self) -> Path | None:
        import tomllib

        config_path = self.__get_config_path()
        if config_path is None:
            return None
        try:
            with config_path.open("rb") as config_file:
                data = tomllib.load(config_file)
        except tomllib.TOMLDecodeError as error:
            raise ConfigurationError(f"Invalid TOML configuration: {config_path}") from error

        adrpy_config = self.__get_adrpy_config(data, config_path)
        if adrpy_config is None:
            return None
        adr_dir = adrpy_config.get("dir")
        if not isinstance(adr_dir, str) or not adr_dir.strip():
            raise ConfigurationError(
                f"Configuration field 'dir' must be a non-empty string: {config_path}"
            )
        return (config_path.parent / adr_dir).resolve()

    def __get_config_path(self) -> Path | None:
        if self.config_path:
            config_path = self.config_path.expanduser()
            if not config_path.is_absolute():
                config_path = self.working_directory / config_path
            if not config_path.is_file():
                raise ConfigurationError(f"Configuration file does not exist: {config_path}")
            return config_path.resolve()

        explicit_config = self.working_directory / ".adrpy.toml"
        if explicit_config.is_file():
            return explicit_config

        pyproject = self.working_directory / "pyproject.toml"
        if pyproject.is_file():
            return pyproject
        return None

    @staticmethod
    def __get_adrpy_config(data: dict[str, object], config_path: Path) -> dict[str, object] | None:
        config_value: object
        # Standalone ADR-py config files use a top-level ``dir`` key. This
        # applies to ``.adrpy.toml`` and to explicitly supplied config paths;
        # pyproject.toml keeps the conventional [tool.adrpy] namespace.
        if config_path.name != "pyproject.toml" and "dir" in data:
            config_value = data
        else:
            tools_value = data.get("tool", {})
            if not isinstance(tools_value, dict):
                raise ConfigurationError(
                    f"Configuration section 'tool' must be a table: {config_path}"
                )
            tools = cast(dict[str, object], tools_value)
            config_value = tools.get("adrpy")
            if config_value is None:
                return None
        if not isinstance(config_value, dict):
            raise ConfigurationError(
                f"Configuration section 'adrpy' must be a table: {config_path}"
            )
        return cast(dict[str, object], config_value)
