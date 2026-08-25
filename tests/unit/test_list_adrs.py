from unittest.mock import Mock

import pytest

from adrpy.shared_kernel.dtos import AdrDocument
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata
from adrpy.use_cases.list_adrs import ListAdrs


def test_should_list_adrs_sorted_by_ordinal_and_mark_superseded() -> None:
    repository = Mock()
    metadata_service = Mock()
    repository.list_documents.return_value = (
        AdrDocument(
            filename="0002-new.md",
            content="new",
        ),
        AdrDocument(
            filename="0001-old.md",
            content="old",
        ),
    )
    metadata_service.parse_document.side_effect = [
        _metadata(2, "New decision", "accepted"),
        _metadata(
            1, "Old decision", "accepted", superseded_by="12345678-1234-5678-1234-567812345678"
        ),
    ]
    original_repository = ListAdrs.REPOSITORY
    original_metadata_service = ListAdrs.METADATA_SERVICE
    ListAdrs.REPOSITORY = repository
    ListAdrs.METADATA_SERVICE = metadata_service

    try:
        items = ListAdrs.execute()
    finally:
        ListAdrs.REPOSITORY = original_repository
        ListAdrs.METADATA_SERVICE = original_metadata_service

    assert [item.ordinal for item in items] == [1, 2]
    assert items[0].is_superseded is True
    assert items[1].is_superseded is False


def test_should_include_filename_when_metadata_is_invalid() -> None:
    repository = Mock()
    repository.list_documents.return_value = (AdrDocument(filename="bad.md", content="bad"),)
    metadata_service = Mock()
    metadata_service.parse_document.side_effect = MetadataValidationError("missing id")
    original_repository = ListAdrs.REPOSITORY
    original_metadata_service = ListAdrs.METADATA_SERVICE
    ListAdrs.REPOSITORY = repository
    ListAdrs.METADATA_SERVICE = metadata_service

    try:
        with pytest.raises(MetadataValidationError, match="bad.md: missing id"):
            ListAdrs.execute()
    finally:
        ListAdrs.REPOSITORY = original_repository
        ListAdrs.METADATA_SERVICE = original_metadata_service


def _metadata(
    ordinal: int, title: str, status: str, superseded_by: str | None = None
) -> AdrMetadata:
    return AdrMetadata(
        id=f"12345678-1234-5678-1234-5678123456{ordinal:02d}",
        ordinal=ordinal,
        title=title,
        status=status,
        date="2026-08-25",
        superseded_by=superseded_by,
    )
