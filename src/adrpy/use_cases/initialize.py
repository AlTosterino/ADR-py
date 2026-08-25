from datetime import datetime
from typing import Final
from uuid import uuid4

from adrpy.injection.container import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.metadata.base import IMetadataService
from adrpy.services.template.base import ITemplateService
from adrpy.shared_kernel.dtos import InitializeAdrDto
from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class InitializeAdr:
    TEMPLATE_SERVICE: Final[ITemplateService] = lidi.resolve_attr(ITemplateService)
    ADR_REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)
    METADATA_SERVICE: Final[IMetadataService] = lidi.resolve_attr(IMetadataService)

    INITIAL_ADR_NAME: Final[str] = "0001-record-architecture-decisions"

    @classmethod
    def execute(cls, dto: InitializeAdrDto) -> None:
        app_template = cls.ADR_REPOSITORY.get_template(name=dto.adr_template_name)
        metadata = AdrMetadata(
            id=str(uuid4()),
            ordinal=1,
            title="Record architecture decisions",
            status=dto.status,
            date=datetime.now().date().isoformat(),
            tags=dto.tags,
        )
        rendered_template = cls.TEMPLATE_SERVICE.render(
            template_file=app_template,
            data={
                "date_created": datetime.now(),
                "status": metadata.status.upper(),
                "front_matter": cls.METADATA_SERVICE.render_front_matter(metadata),
            },
        )
        cls.ADR_REPOSITORY.create(adr_name=cls.INITIAL_ADR_NAME, template=rendered_template)
