from collections import defaultdict
from typing import Final

from adrpy.injection.container import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.metadata.base import IMetadataService
from adrpy.shared_kernel.dtos import AdrCheckDiagnostic, AdrCheckReport
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class CheckAdrs:
    """Validate metadata and relationships across the configured ADR collection."""

    REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)
    METADATA_SERVICE: Final[IMetadataService] = lidi.resolve_attr(IMetadataService)

    @classmethod
    def execute(cls) -> AdrCheckReport:
        documents = cls.REPOSITORY.list_documents()
        diagnostics: list[AdrCheckDiagnostic] = []
        valid_records: list[tuple[str, AdrMetadata]] = []

        for document in documents:
            try:
                metadata = cls.METADATA_SERVICE.parse_document(document.content)
            except MetadataValidationError as error:
                diagnostics.append(
                    AdrCheckDiagnostic(filename=document.filename, message=str(error))
                )
                continue
            valid_records.append((document.filename, metadata))
            cls.__check_filename_ordinal(document.filename, metadata, diagnostics)

        diagnostics.extend(cls.__duplicate_diagnostics(valid_records, "id"))
        diagnostics.extend(cls.__duplicate_diagnostics(valid_records, "ordinal"))
        diagnostics.extend(cls.__relationship_diagnostics(valid_records))
        return AdrCheckReport(checked_files=len(documents), diagnostics=tuple(diagnostics))

    @staticmethod
    def __check_filename_ordinal(
        filename: str, metadata: AdrMetadata, diagnostics: list[AdrCheckDiagnostic]
    ) -> None:
        prefix = filename.split("-", 1)[0]
        if not prefix.isdigit():
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message="filename must start with a numeric ordinal",
                )
            )
            return
        filename_ordinal = int(prefix)
        if filename_ordinal != metadata.ordinal:
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message=(
                        f"filename ordinal {filename_ordinal} does not match metadata ordinal "
                        f"{metadata.ordinal}"
                    ),
                )
            )

    @staticmethod
    def __duplicate_diagnostics(
        records: list[tuple[str, AdrMetadata]], field_name: str
    ) -> list[AdrCheckDiagnostic]:
        grouped: dict[object, list[str]] = defaultdict(list)
        for filename, metadata in records:
            grouped[getattr(metadata, field_name)].append(filename)

        diagnostics: list[AdrCheckDiagnostic] = []
        for value, filenames in grouped.items():
            if len(filenames) > 1:
                for filename in sorted(filenames):
                    other_filenames = ", ".join(
                        other for other in sorted(filenames) if other != filename
                    )
                    diagnostics.append(
                        AdrCheckDiagnostic(
                            filename=filename,
                            message=(
                                f"duplicate {field_name} '{value}' also appears in "
                                f"{other_filenames}"
                            ),
                        )
                    )
        return diagnostics

    @classmethod
    def __relationship_diagnostics(
        cls, records: list[tuple[str, AdrMetadata]]
    ) -> list[AdrCheckDiagnostic]:
        by_id = {metadata.id: (filename, metadata) for filename, metadata in records}
        diagnostics: list[AdrCheckDiagnostic] = []
        edges: dict[str, set[str]] = defaultdict(set)

        for filename, metadata in records:
            for target_id in metadata.supersedes:
                edges[metadata.id].add(target_id)
                cls.__check_supersedes_link(filename, metadata, target_id, by_id, diagnostics)
            if metadata.superseded_by is not None:
                edges[metadata.superseded_by].add(metadata.id)
                cls.__check_superseded_by_link(filename, metadata, by_id, diagnostics)
            if metadata.id in metadata.supersedes or metadata.superseded_by == metadata.id:
                diagnostics.append(
                    AdrCheckDiagnostic(
                        filename=filename,
                        message="ADR cannot supersede itself",
                    )
                )

        diagnostics.extend(cls.__cycle_diagnostics(records, edges))
        return diagnostics

    @staticmethod
    def __check_supersedes_link(
        filename: str,
        metadata: AdrMetadata,
        target_id: str,
        by_id: dict[str, tuple[str, AdrMetadata]],
        diagnostics: list[AdrCheckDiagnostic],
    ) -> None:
        target = by_id.get(target_id)
        if target is None:
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message=f"supersedes references missing ADR UUID {target_id}",
                )
            )
            return
        target_filename, target_metadata = target
        if target_metadata.superseded_by != metadata.id:
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message=(
                        f"supersedes {target_filename}, but its superseded_by field is not "
                        f"{metadata.id}"
                    ),
                )
            )

    @staticmethod
    def __check_superseded_by_link(
        filename: str,
        metadata: AdrMetadata,
        by_id: dict[str, tuple[str, AdrMetadata]],
        diagnostics: list[AdrCheckDiagnostic],
    ) -> None:
        replacement_id = metadata.superseded_by
        assert replacement_id is not None
        replacement = by_id.get(replacement_id)
        if replacement is None:
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message=f"superseded_by references missing ADR UUID {replacement_id}",
                )
            )
            return
        replacement_filename, replacement_metadata = replacement
        if metadata.id not in replacement_metadata.supersedes:
            diagnostics.append(
                AdrCheckDiagnostic(
                    filename=filename,
                    message=(
                        f"superseded_by references {replacement_filename}, but that ADR does "
                        f"not list {metadata.id} in supersedes"
                    ),
                )
            )

    @staticmethod
    def __cycle_diagnostics(
        records: list[tuple[str, AdrMetadata]], edges: dict[str, set[str]]
    ) -> list[AdrCheckDiagnostic]:
        filenames = {metadata.id: filename for filename, metadata in records}
        visited: set[str] = set()
        active: set[str] = set()
        diagnostics: list[AdrCheckDiagnostic] = []

        def visit(node: str) -> None:
            if node in active:
                diagnostics.append(
                    AdrCheckDiagnostic(
                        filename=filenames.get(node, node),
                        message="supersession relationships contain a cycle",
                    )
                )
                return
            if node in visited:
                return
            active.add(node)
            for target in sorted(edges.get(node, ())):
                if target in filenames:
                    visit(target)
            active.remove(node)
            visited.add(node)

        for node in sorted(filenames):
            visit(node)
        return diagnostics
