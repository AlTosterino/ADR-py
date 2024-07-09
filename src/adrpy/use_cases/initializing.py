from dataclasses import dataclass, field
from datetime import datetime

from adrpy.injection import lidi
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.dtos import InitializeADRDTO


@dataclass
class InitializingADR:
    template_service = lidi.resolve_attr(BaseTemplateService)
    file_service = lidi.resolve_attr(BaseADRRepository)
    INITIAL_ADR_NAME: str = field(init=False, default="0001-record-architecture-decisions")

    def execute(self, dto: InitializeADRDTO) -> None:
        app_template = self.file_service.get_template(name=dto.adr_template_name)
        rendered_template = self.template_service.render(
            template_file=app_template, data={"date_created": datetime.now(), "status": "ACCEPTED"}
        )
        self.file_service.create(adr_name=self.INITIAL_ADR_NAME, template=rendered_template)
