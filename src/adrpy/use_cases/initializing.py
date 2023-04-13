from dataclasses import dataclass

from adrpy.injection import Inject
from adrpy.services.file.base import BaseFileService
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import InitializeADRDTO
from adrpy.shared_kernel.settings import Settings
from loguru import logger

INITIAL_FILENAME = "0001-record-architecture-decisions.md"

@dataclass
class InitializingADR:
    template_service: Inject[BaseTemplateService]
    file_service: Inject[BaseFileService]
    settings: Inject[Settings]

    def execute(self, dto: InitializeADRDTO) -> None:
        app_template_file = self.file_service.get_file(path=dto.adr_template_path)
        rendered_template = self.template_service.render(
            template_file=app_template_file, data={"date": "TODAY", "status": "ACCEPTED"}
        )
        save_path = dto.path
        if not save_path:
            save_path = self.settings.adr_dir
            logger.info("Initializing ADR in directory from config file")
        else:
            logger.info(f"Initializing ADR in: {save_path}")
        self.file_service.create_file(
            path=save_path,
            filename=INITIAL_FILENAME,
            content=rendered_template.content,
        )
