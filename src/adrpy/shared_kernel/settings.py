from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from loguru import logger


@dataclass(frozen=True)
class Settings:
    debug: bool = False
    initial_adr_dir: Path | None = None  # TODO: Rename to requested_adr_dir or something
    APP_TEMPLATES_DIR: Path = field(init=False, default=Path(__file__).parents[1] / "templates")

    def __post_init__(self) -> None:
        logger.debug(self)

    @cached_property
    def adr_dir(self) -> Path | None:
        if self.initial_adr_dir:
            logger.debug("Using initial adr dir: {}", self.initial_adr_dir)
            return self.initial_adr_dir
        if adr_dir_from_config := self.__get_adr_dir_from_config():
            logger.debug("Using adr dir from config: {}", adr_dir_from_config)
            return adr_dir_from_config
        logger.debug("Using working directory as adr dir: {}", self.working_directory)
        return self.working_directory

    @cached_property
    def working_directory(self) -> Path:
        return Path.cwd()

    def __get_adr_dir_from_config(self) -> Path | None:
        import tomllib

        logger.debug("Trying to get ADR directory from pyproject.toml")
        with logger.contextualize(working_directory=self.working_directory):
            try:
                with open(self.working_directory / "pyproject.toml", "rb") as f:
                    data = tomllib.load(f)
            except FileNotFoundError:
                logger.debug("No pyproject.toml found in working directory")
                return None
            tools = data.get("tool", {})
            adrpy_tool = tools.get("adrpy", {})
            adrpy_dir = adrpy_tool.get("dir", None)
            if adrpy_dir:
                full_path: Path = self.working_directory / adrpy_dir
                return full_path
            return None
