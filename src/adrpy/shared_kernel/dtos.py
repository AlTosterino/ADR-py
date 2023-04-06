from dataclasses import dataclass, field
from pathlib import Path

from adrpy.shared_kernel.constants import AppTemplatePaths


@dataclass(frozen=True)
class InitializeADRDTO:
    path: Path
    adr_template_path: Path = field(default=AppTemplatePaths.INITIAL_ADR, init=False)
