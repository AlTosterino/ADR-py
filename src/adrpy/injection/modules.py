from injector import Binder, singleton

from adrpy.services.file.service import BaseFileService, FileService
from adrpy.services.template.service import BaseTemplateService, MakoTemplateService


def configure_modules(binder: Binder) -> None:
    binder.bind(BaseFileService, to=FileService(), scope=singleton)
    binder.bind(BaseTemplateService, to=MakoTemplateService(), scope=singleton)
