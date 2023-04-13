from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class File:
    path: Path
    content: str

@dataclass(frozen=True)
class RenderedFile(File):
    pass
