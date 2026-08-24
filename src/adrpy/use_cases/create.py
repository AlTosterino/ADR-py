from datetime import datetime
from typing import Final
from uuid import uuid4

from adrpy.injection import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.metadata.base import IMetadataService
from adrpy.services.template.base import ITemplateService
from adrpy.shared_kernel.dtos import CreateAdrDto
from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class CreateAdr:
    TEMPLATE_SERVICE: Final[ITemplateService] = lidi.resolve_attr(ITemplateService)
    REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)
    METADATA_SERVICE: Final[IMetadataService] = lidi.resolve_attr(IMetadataService)

    @classmethod
    def execute(cls, dto: CreateAdrDto) -> None:
        template = cls.REPOSITORY.get_template(name=dto.adr_template_name)
        ordinal_number = cls.REPOSITORY.get_next_ordinal_number()
        metadata = AdrMetadata(
            id=str(uuid4()),
            ordinal=ordinal_number,
            title=dto.name,
            status="accepted",
            date=datetime.now().date().isoformat(),
        )
        rendered_template = cls.TEMPLATE_SERVICE.render(
            template_file=template,
            data={
                "date_created": datetime.now(),
                "status": metadata.status.upper(),
                "name": dto.name,
                "ordinal_num": ordinal_number,
                "front_matter": cls.METADATA_SERVICE.render_front_matter(metadata),
            },
        )
        adr_name = dto.adr_name_with_ordinal(ordinal_number=ordinal_number)
        cls.REPOSITORY.create(adr_name=adr_name, template=rendered_template)
