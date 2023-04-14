from dataclasses import dataclass

from adrpy.injection import Inject
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import CreateADRDTO


@dataclass
class CreatingADR:
    template_service: Inject[BaseTemplateService]
    adr_repository: Inject[BaseADRRepository]

    def execute(self, dto: CreateADRDTO) -> None:
        template = self.adr_repository.get_template(name=dto.adr_template_name)
        rendered_template = self.template_service.render(
            template_file=template,
            data={"date": "TODAY", "status": "ACCEPTED", "name": dto.name, "ordinal_num": 1},
        )
        ordinal_number = self.adr_repository.get_next_ordinal_number()
        adr_name = dto.adr_name_with_ordinal(ordinal_number=ordinal_number)
        self.adr_repository.create(adr_name=adr_name, template=rendered_template)