from unittest.mock import Mock

from adrpy.shared_kernel.dtos import AdrCheckReport, AdrDocument
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata
from adrpy.use_cases.check_adrs import CheckAdrs

FIRST_ID = "11111111-1111-1111-1111-111111111111"
SECOND_ID = "22222222-2222-2222-2222-222222222222"
THIRD_ID = "33333333-3333-3333-3333-333333333333"
EXPECTED_FILE_COUNT = 2


def test_should_accept_isolated_and_consistent_supersession_records() -> None:
    first = _metadata(FIRST_ID, 1, "Record decisions")
    second = _metadata(SECOND_ID, 2, "Use PostgreSQL", supersedes=(FIRST_ID,))
    first = _metadata(FIRST_ID, 1, "Record decisions", superseded_by=SECOND_ID)

    report = _run_check(
        (AdrDocument("0001-record.md", "first"), AdrDocument("0002-postgresql.md", "second")),
        (first, second),
    )

    assert report == AdrCheckReport(checked_files=2)


def test_should_report_duplicates_missing_links_and_filename_mismatch() -> None:
    first = _metadata(FIRST_ID, 1, "First", superseded_by=THIRD_ID)
    duplicate = _metadata(FIRST_ID, 1, "Duplicate")

    report = _run_check(
        (AdrDocument("0001-first.md", "first"), AdrDocument("0003-duplicate.md", "duplicate")),
        (first, duplicate),
    )

    messages = _messages(report)
    assert any("duplicate id" in message for message in messages)
    assert any("duplicate ordinal" in message for message in messages)
    assert any("missing ADR UUID" in message for message in messages)
    assert any("does not match metadata ordinal" in message for message in messages)


def test_should_report_contradictory_links_and_cycles() -> None:
    first = _metadata(FIRST_ID, 1, "First", supersedes=(SECOND_ID,))
    second = _metadata(SECOND_ID, 2, "Second", supersedes=(FIRST_ID,))

    report = _run_check(
        (AdrDocument("0001-first.md", "first"), AdrDocument("0002-second.md", "second")),
        (first, second),
    )

    messages = _messages(report)
    assert any("superseded_by field" in message for message in messages)
    assert any("cycle" in message for message in messages)


def test_should_report_malformed_metadata_and_continue_checking() -> None:
    repository = Mock()
    repository.list_documents.return_value = (
        AdrDocument("0001-invalid.md", "invalid"),
        AdrDocument("0002-valid.md", "valid"),
    )
    metadata_service = Mock()
    metadata_service.parse_document.side_effect = [
        MetadataValidationError("missing id"),
        _metadata(SECOND_ID, 2, "Valid"),
    ]
    original_repository = CheckAdrs.REPOSITORY
    original_metadata_service = CheckAdrs.METADATA_SERVICE
    CheckAdrs.REPOSITORY = repository
    CheckAdrs.METADATA_SERVICE = metadata_service

    try:
        report = CheckAdrs.execute()
    finally:
        CheckAdrs.REPOSITORY = original_repository
        CheckAdrs.METADATA_SERVICE = original_metadata_service

    assert report.checked_files == EXPECTED_FILE_COUNT
    assert report.diagnostics[0].filename == "0001-invalid.md"
    assert report.diagnostics[0].message == "missing id"


def _run_check(
    documents: tuple[AdrDocument, ...], metadata: tuple[AdrMetadata, ...]
) -> AdrCheckReport:
    repository = Mock()
    repository.list_documents.return_value = documents
    metadata_service = Mock()
    metadata_service.parse_document.side_effect = metadata
    original_repository = CheckAdrs.REPOSITORY
    original_metadata_service = CheckAdrs.METADATA_SERVICE
    CheckAdrs.REPOSITORY = repository
    CheckAdrs.METADATA_SERVICE = metadata_service

    try:
        return CheckAdrs.execute()
    finally:
        CheckAdrs.REPOSITORY = original_repository
        CheckAdrs.METADATA_SERVICE = original_metadata_service


def _metadata(
    identifier: str,
    ordinal: int,
    title: str,
    supersedes: tuple[str, ...] = (),
    superseded_by: str | None = None,
) -> AdrMetadata:
    return AdrMetadata(
        id=identifier,
        ordinal=ordinal,
        title=title,
        status="superseded" if superseded_by else "accepted",
        date="2026-08-25",
        supersedes=supersedes,
        superseded_by=superseded_by,
    )


def _messages(report: AdrCheckReport) -> tuple[str, ...]:
    return tuple(diagnostic.message for diagnostic in report.diagnostics)
