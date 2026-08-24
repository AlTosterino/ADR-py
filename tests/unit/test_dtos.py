from pathlib import Path

import pytest

from adrpy.shared_kernel.dtos import CreateAdrDto, InitializeAdrDto
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrCreationMetadata


def test_creation_metadata_defaults_to_proposed_without_tags() -> None:
    dto = CreateAdrDto(name="Use PostgreSQL")

    assert dto.status == "proposed"
    assert dto.tags == ()


def test_creation_metadata_is_a_named_value_object() -> None:
    metadata = AdrCreationMetadata(status="proposed", tags=("architecture",))

    assert metadata.status == "proposed"
    assert metadata.tags == ("architecture",)


def test_creation_metadata_trims_tags_and_preserves_order() -> None:
    dto = InitializeAdrDto(path=Path("docs/adr"), tags=(" database ", "persistence"))

    assert dto.tags == ("database", "persistence")


def test_creation_metadata_rejects_duplicate_tags() -> None:
    with pytest.raises(MetadataValidationError, match="duplicates"):
        CreateAdrDto(name="Use PostgreSQL", tags=("database", "database"))


def test_creation_metadata_rejects_unknown_status() -> None:
    with pytest.raises(MetadataValidationError, match="status"):
        CreateAdrDto(name="Use PostgreSQL", status="draft")
