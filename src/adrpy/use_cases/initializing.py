from dataclasses import dataclass

from adrpy.injection import Inject
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import InitializeADRDTO


@dataclass
class InitializingADR:
    template_service: Inject[BaseTemplateService]

    def execute(self, dto: InitializeADRDTO) -> None:
        app_template = self.template_service.get_template(template_name=dto.template_type)
        rendered_template = self.template_service.render(
            template=app_template, data={"date": "TODAY", "status": "ACCEPTED"}
        )
        with open(dto.path / dto.adr_name, "w") as file:
            file.write(rendered_template.content)
        print("DONE")
