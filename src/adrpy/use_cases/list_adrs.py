from typing import Final

from adrpy.injection.container import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.metadata.base import IMetadataService
from adrpy.shared_kernel.dtos import AdrListItem
from adrpy.shared_kernel.errors import MetadataValidationError


class ListAdrs:
    """Load and validate the ADRs available in the configured repository."""

    REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)
    METADATA_SERVICE: Final[IMetadataService] = lidi.resolve_attr(IMetadataService)

    @classmethod
    def execute(cls) -> tuple[AdrListItem, ...]:
        items = []
        for document in cls.REPOSITORY.list_documents():
            try:
                metadata = cls.METADATA_SERVICE.parse_document(document.content)
            except MetadataValidationError as error:
                raise MetadataValidationError(f"{document.filename}: {error}") from error
            items.append(
                AdrListItem(
                    filename=document.filename,
                    ordinal=metadata.ordinal,
                    title=metadata.title,
                    status=metadata.status,
                    tags=metadata.tags,
                    is_superseded=(
                        metadata.status == "superseded" or metadata.superseded_by is not None
                    ),
                )
            )
        return tuple(sorted(items, key=lambda item: (item.ordinal, item.filename)))
