from adrpy.services.metadata.service import YamlMetadataService
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata

ADR_ID = "12345678-1234-5678-1234-567812345678"


def test_should_round_trip_adr_metadata_through_yaml_front_matter() -> None:
    metadata = AdrMetadata(
        id=ADR_ID,
        ordinal=7,
        title="Use PostgreSQL",
        status="accepted",
        date="2026-08-24",
        tags=("database", "persistence"),
    )
    service = YamlMetadataService()

    document = f"{service.render_front_matter(metadata)}\n\n# Use PostgreSQL\n"

    assert service.parse_document(document) == metadata
    assert "tags:\n- database\n- persistence" in document


def test_should_render_empty_metadata_collections_as_yaml_lists() -> None:
    metadata = AdrMetadata(
        id=ADR_ID,
        ordinal=1,
        title="Record architecture decisions",
        status="accepted",
        date="2026-08-24",
    )

    front_matter = YamlMetadataService().render_front_matter(metadata)

    assert "tags: []" in front_matter
    assert "supersedes: []" in front_matter
    assert "superseded_by: null" in front_matter


def test_should_reject_front_matter_without_required_fields() -> None:
    with_exception = "---\ntitle: Missing ID\n---\n\n# Missing ID\n"

    try:
        YamlMetadataService().parse_document(with_exception)
    except MetadataValidationError as error:
        assert "missing" in str(error)
    else:
        raise AssertionError("Expected MetadataValidationError")


def test_should_allow_human_readable_tags_but_validate_uuid_relationships() -> None:
    metadata = AdrMetadata(
        id=ADR_ID,
        ordinal=2,
        title="Use PostgreSQL",
        status="accepted",
        date="2026-08-24",
        tags=("database",),
    )

    assert metadata.tags == ("database",)
