from dataclasses import dataclass

from adrpy.injection import Inject
from adrpy.services.file.base import BaseFileService
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import InitializeADRDTO


@dataclass
class InitializingADR:
    template_service: Inject[BaseTemplateService]
    file_service: Inject[BaseFileService]

    def execute(self, dto: InitializeADRDTO) -> None:
        app_template = self.file_service.get_file(path=dto.adr_template_path)
        rendered_template = self.template_service.render(
            file=app_template, data={"date": "TODAY", "status": "ACCEPTED"}
        )
        with open(dto.path / dto.adr_name, "w") as file:
            file.write(rendered_template.content)
        print("DONE")
