from lidipy import Lidi

from adrpy.repositories.adr.base import IADRRepository
from adrpy.repositories.adr.repository import ADRFileRepository
from adrpy.services.metadata.base import IMetadataService
from adrpy.services.metadata.service import YamlMetadataService
from adrpy.services.template.base import ITemplateService
from adrpy.services.template.service import MakoTemplateService


def bind_modules(lidi: Lidi) -> None:
    lidi.bind(IADRRepository, ADRFileRepository())
    lidi.bind(IMetadataService, YamlMetadataService())
    lidi.bind(ITemplateService, MakoTemplateService())
