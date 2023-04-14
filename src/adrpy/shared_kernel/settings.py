from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    working_directory: Path = field(default_factory=Path.cwd)
    initial_adr_dir: Path | None = None
    APP_TEMPLATES_DIR: Path = field(init=False, default=Path(__file__).parents[1] / "templates")

    @property
    def adr_dir(self) -> Path | None:
        # TODO: Handle missing dir
        if self.initial_adr_dir:
            return self.initial_adr_dir
        return self.__get_adr_dir_from_pyproject()

    def __get_adr_dir_from_pyproject(self) -> Path | None:
        import tomllib

        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        tools = data.get("tool", {})
        adrpy_tool = tools.get("adrpy", {})
        adrpy_dir = adrpy_tool.get("dir", None)
        if adrpy_dir:
            full_path: Path = self.working_directory / adrpy_dir
            return full_path
        return None
