from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    working_directory: Path

    @property
    def adr_dir(self) -> Path | None:
        return self.__get_adr_dir_from_pyproject()

    def __get_adr_dir_from_pyproject(self) -> Path | None:
        import tomllib

        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        tools = data.get("tool", {})
        adrpy_tool = tools.get("adrpy", {})
        adpry_dir = adrpy_tool.get("dir", None)
        if adpry_dir:
            full_path: Path = self.working_directory / adpry_dir
            return full_path
        return None
