from dataclasses import dataclass
from datetime import datetime

from adrpy.injection import lidi
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import CreateADRDTO


@dataclass
class CreatingADR:
    template_service = lidi.resolve_attr(BaseTemplateService)
    adr_repository = lidi.resolve_attr(BaseADRRepository)

    def execute(self, dto: CreateADRDTO) -> None:
        template = self.adr_repository.get_template(name=dto.adr_template_name)
        rendered_template = self.template_service.render(
            template_file=template,
            data={
                "date_created": datetime.now(),
                "status": "ACCEPTED",
                "name": dto.name,
                "ordinal_num": 1,
            },
        )
        ordinal_number = self.adr_repository.get_next_ordinal_number()
        adr_name = dto.adr_name_with_ordinal(ordinal_number=ordinal_number)
        self.adr_repository.create(adr_name=adr_name, template=rendered_template)
