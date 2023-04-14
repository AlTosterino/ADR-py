from dataclasses import dataclass, field
from pathlib import Path

from adrpy.shared_kernel.constants import AppTemplates


@dataclass(frozen=True)
class InitializeADRDTO:
    path: Path | None
    adr_template_name: str = field(default=AppTemplates.INITIAL_ADR, init=False)


@dataclass(frozen=True)
class CreateADRDTO:
    name: str
    adr_template_name: str = field(default=AppTemplates.NEW_ADR, init=False)

    @property
    def adr_name(self) -> str:
        lower_name = self.name.lower()
        lower_name_no_spaces = "-".join(lower_name.split())
        return lower_name_no_spaces

    def adr_name_with_ordinal(self, ordinal_number: int) -> str:
        return f"{ordinal_number:04d}-{self.adr_name}"
