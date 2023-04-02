from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileTemplate:
    path: Path
    content: str


@dataclass(frozen=True)
class RenderedTemplate(FileTemplate):
    pass
