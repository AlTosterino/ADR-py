from datetime import datetime
from typing import Final

from adrpy.injection import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.services.template.base import ITemplateService
from adrpy.shared_kernel.dtos import InitializeAdrDto


class InitializeAdr:
    TEMPLATE_SERVICE: Final[ITemplateService] = lidi.resolve_attr(ITemplateService)
    ADR_REPOSITORY: Final[IADRRepository] = lidi.resolve_attr(IADRRepository)

    INITIAL_ADR_NAME: Final[str] = "0001-record-architecture-decisions"

    @classmethod
    def execute(cls, dto: InitializeAdrDto) -> None:
        app_template = cls.ADR_REPOSITORY.get_template(name=dto.adr_template_name)
        rendered_template = cls.TEMPLATE_SERVICE.render(
            template_file=app_template, data={"date_created": datetime.now(), "status": "ACCEPTED"}
        )
        cls.ADR_REPOSITORY.create(adr_name=cls.INITIAL_ADR_NAME, template=rendered_template)
