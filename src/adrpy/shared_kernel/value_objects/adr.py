from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from adrpy.shared_kernel.errors import MetadataValidationError

VALID_STATUSES = frozenset({"proposed", "accepted", "rejected", "deprecated", "superseded"})


def validate_status(value: str) -> str:
    if value not in VALID_STATUSES:
        statuses = ", ".join(sorted(VALID_STATUSES))
        raise MetadataValidationError(f"Metadata field 'status' must be one of: {statuses}")
    return value


def normalize_tags(values: Iterable[str]) -> tuple[str, ...]:
    tags = tuple(tag.strip() for tag in values)
    if any(not tag for tag in tags):
        raise MetadataValidationError("Metadata field 'tags' must contain non-empty strings")
    if len(tags) != len(set(tags)):
        raise MetadataValidationError("Metadata field 'tags' must not contain duplicates")
    return tags


@dataclass(frozen=True)
class AdrMetadata:
    id: str
    ordinal: int
    title: str
    status: str
    date: str
    tags: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    superseded_by: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise MetadataValidationError("Metadata field 'id' must be a UUID string")
        try:
            normalized_id = str(UUID(self.id))
        except (ValueError, AttributeError) as error:
            raise MetadataValidationError("Metadata field 'id' must be a valid UUID") from error
        object.__setattr__(self, "id", normalized_id)

        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 1:
            raise MetadataValidationError("Metadata field 'ordinal' must be a positive integer")
        if not isinstance(self.title, str) or not self.title.strip():
            raise MetadataValidationError("Metadata field 'title' must not be empty")
        if not isinstance(self.status, str):
            raise MetadataValidationError("Metadata field 'status' must be a string")
        validate_status(self.status)
        try:
            if not isinstance(self.date, str):
                raise ValueError
            date.fromisoformat(self.date)
        except (TypeError, ValueError) as error:
            raise MetadataValidationError(
                "Metadata field 'date' must use ISO format YYYY-MM-DD"
            ) from error
        if not all(isinstance(tag, str) for tag in self.tags):
            raise MetadataValidationError("Metadata field 'tags' must contain non-empty strings")
        object.__setattr__(self, "tags", normalize_tags(self.tags))
        self.__validate_references(self.supersedes, "supersedes")
        if self.superseded_by is not None:
            self.__validate_references((self.superseded_by,), "superseded_by")

    def to_mapping(self) -> dict[str, object]:
        return {
            "id": self.id,
            "ordinal": self.ordinal,
            "title": self.title,
            "status": self.status,
            "date": self.date,
            "tags": list(self.tags),
            "supersedes": list(self.supersedes),
            "superseded_by": self.superseded_by,
        }

    @classmethod
    def from_mapping(cls, data: object) -> "AdrMetadata":
        if not isinstance(data, dict):
            raise MetadataValidationError("ADR front matter must be a YAML mapping")

        required = ("id", "ordinal", "title", "status", "date")
        missing = [field for field in required if field not in data]
        if missing:
            raise MetadataValidationError(f"ADR front matter is missing: {', '.join(missing)}")

        return cls(
            id=data["id"],
            ordinal=data["ordinal"],
            title=data["title"],
            status=data["status"],
            date=data["date"],
            tags=cls.__as_string_tuple(data.get("tags", []), "tags"),
            supersedes=cls.__as_string_tuple(data.get("supersedes", []), "supersedes"),
            superseded_by=cls.__as_optional_string(data.get("superseded_by"), "superseded_by"),
        )

    @staticmethod
    def __as_string_tuple(value: object, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise MetadataValidationError(
                f"Metadata field '{field_name}' must be a list of strings"
            )
        return tuple(value)

    @staticmethod
    def __as_optional_string(value: object, field_name: str) -> str | None:
        if value is not None and not isinstance(value, str):
            raise MetadataValidationError(f"Metadata field '{field_name}' must be a string or null")
        return value

    @staticmethod
    def __validate_references(values: tuple[str, ...], field_name: str) -> None:
        for value in values:
            try:
                UUID(value)
            except (ValueError, AttributeError) as error:
                raise MetadataValidationError(
                    f"Metadata field '{field_name}' must contain valid UUIDs"
                ) from error
