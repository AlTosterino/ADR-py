from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # TODO: Add DEBUG logger handler
    working_directory: Path = field(default_factory=Path.cwd)
    initial_adr_dir: Path | None = None  # TODO: Rename to requested_adr_dir or something
    APP_TEMPLATES_DIR: Path = field(init=False, default=Path(__file__).parents[1] / "templates")

    @property
    def adr_dir(self) -> Path | None:
        if self.initial_adr_dir:
            return self.initial_adr_dir
        if adr_dir_from_config := self.__get_adr_dir_from_config():
            return adr_dir_from_config
        return self.working_directory

    def __get_adr_dir_from_config(self) -> Path | None:
        import tomllib

        try:
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
        except FileNotFoundError:
            # TODO): Add debug log here
            return None
        tools = data.get("tool", {})
        adrpy_tool = tools.get("adrpy", {})
        adrpy_dir = adrpy_tool.get("dir", None)
        if adrpy_dir:
            full_path: Path = self.working_directory / adrpy_dir
            return full_path
        return None
