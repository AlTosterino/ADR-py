from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.repositories.adr.repository import ADRFileRepository
from adrpy.services.template.base import BaseTemplateService
from adrpy.services.template.service import MakoTemplateService
from adrpy.shared_kernel.settings import Settings
from lidipy import Lidi


def bind_modules(lidi: Lidi) -> None:
    lidi.bind(BaseADRRepository, ADRFileRepository(settings=lidi.resolve(Settings)))
    lidi.bind(BaseTemplateService, MakoTemplateService())
