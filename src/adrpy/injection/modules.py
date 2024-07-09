from lidipy import Lidi


def bind_modules(lidi: Lidi) -> None:
    from adrpy.repositories.adr.base import BaseADRRepository
    from adrpy.repositories.adr.repository import ADRFileRepository
    from adrpy.services.template.base import BaseTemplateService
    from adrpy.services.template.service import MakoTemplateService

    lidi.bind(BaseADRRepository, ADRFileRepository())
    lidi.bind(BaseTemplateService, MakoTemplateService())
