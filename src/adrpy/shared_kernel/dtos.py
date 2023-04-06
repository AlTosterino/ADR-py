from dataclasses import dataclass
from pathlib import Path

from adrpy.shared_kernel.enums import AppTemplates


@dataclass(frozen=True)
class InitializeADRDTO:
    path: Path
    template_type: AppTemplates
    adr_name: str = "0001-record-architecture-decisions.md"
