from dataclasses import dataclass, field
from pathlib import Path

from adrpy.shared_kernel.constants import AppTemplates
from adrpy.shared_kernel.value_objects.adr import normalize_tags, validate_status


@dataclass(frozen=True)
class AdrDocument:
    """An ADR file loaded from the configured repository."""

    filename: str
    content: str


@dataclass(frozen=True)
class AdrListItem:
    """Validated metadata displayed by the ADR listing command."""

    filename: str
    ordinal: int
    title: str
    status: str
    tags: tuple[str, ...]
    is_superseded: bool


@dataclass(frozen=True)
class InitializeAdrDto:
    path: Path | None
    config_path: Path | None = None
    status: str = "proposed"
    tags: tuple[str, ...] = ()
    adr_template_name: str = field(default=AppTemplates.INITIAL_ADR, init=False)

    def __post_init__(self) -> None:
        validate_status(self.status)
        object.__setattr__(self, "tags", normalize_tags(self.tags))


@dataclass(frozen=True)
class CreateAdrDto:
    name: str
    config_path: Path | None = None
    status: str = "proposed"
    tags: tuple[str, ...] = ()
    adr_template_name: str = field(default=AppTemplates.NEW_ADR, init=False)

    def __post_init__(self) -> None:
        validate_status(self.status)
        object.__setattr__(self, "tags", normalize_tags(self.tags))

    @property
    def adr_name(self) -> str:
        lower_name = self.name.lower()
        lower_name_no_spaces = "-".join(lower_name.split())
        return lower_name_no_spaces

    def adr_name_with_ordinal(self, ordinal_number: int) -> str:
        return f"{ordinal_number:04d}-{self.adr_name}"
