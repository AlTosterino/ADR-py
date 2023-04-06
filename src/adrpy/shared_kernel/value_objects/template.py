from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class File:
    path: Path
    content: str

    @property
    def filename(self) -> str:
        return self.path.name


@dataclass(frozen=True)
class RenderedFile(File):
    pass
