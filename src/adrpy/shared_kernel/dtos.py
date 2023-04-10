from dataclasses import dataclass, field
from pathlib import Path

from adrpy.shared_kernel.constants import AppTemplatePaths


@dataclass(frozen=True)
class InitializeADRDTO:
    path: Path | None
    adr_template_path: Path = field(default=AppTemplatePaths.INITIAL_ADR, init=False)


@dataclass(frozen=True)
class CreateADRDTO:
    name: str
    adr_template_path: Path = field(default=AppTemplatePaths.NEW_ADR, init=False)
