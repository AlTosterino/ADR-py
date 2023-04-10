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
        app_template_file = self.file_service.get_file(path=dto.adr_template_path)
        rendered_template = self.template_service.render(
            template_file=app_template_file, data={"date": "TODAY", "status": "ACCEPTED"}
        )
        self.file_service.create_file(
            path=dto.path, filename=rendered_template.filename, content=rendered_template.content
        )
