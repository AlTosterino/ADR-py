from datetime import datetime
from typing import Final

from adrpy.injection import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.template.base import ITemplateService
from adrpy.shared_kernel.dtos import CreateAdrDto


class CreateAdr:
    TEMPLATE_SERVICE: Final[ITemplateService] = lidi.resolve_attr(ITemplateService)
    REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)

    @classmethod
    def execute(cls, dto: CreateAdrDto) -> None:
        template = cls.REPOSITORY.get_template(name=dto.adr_template_name)
        ordinal_number = cls.REPOSITORY.get_next_ordinal_number()
        rendered_template = cls.TEMPLATE_SERVICE.render(
            template_file=template,
            data={
                "date_created": datetime.now(),
                "status": "ACCEPTED",
                "name": dto.name,
                "ordinal_num": ordinal_number,
            },
        )
        adr_name = dto.adr_name_with_ordinal(ordinal_number=ordinal_number)
        cls.REPOSITORY.create(adr_name=adr_name, template=rendered_template)
