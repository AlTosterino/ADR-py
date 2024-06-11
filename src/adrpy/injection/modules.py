from lidipy import Lidi


def bind_modules(lidi: Lidi) -> None:
    from adrpy.repositories.adr.base import IADRRepository
    from adrpy.repositories.adr.repository import ADRFileRepository
    from adrpy.services.template.base import ITemplateService
    from adrpy.services.template.service import MakoTemplateService

    lidi.bind(IADRRepository, ADRFileRepository())
    lidi.bind(ITemplateService, MakoTemplateService())
