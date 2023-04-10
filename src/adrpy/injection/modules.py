from adrpy.services.file.service import BaseFileService, FileService
from adrpy.services.template.service import BaseTemplateService, MakoTemplateService
from injector import Binder, singleton


def configure_modules(binder: Binder) -> None:
    binder.bind(BaseFileService, to=FileService(), scope=singleton)
    binder.bind(BaseTemplateService, to=MakoTemplateService(), scope=singleton)
