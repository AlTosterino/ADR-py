from injector import Binder, singleton


def configure_modules(binder: Binder) -> None:
    from adrpy.services.template.service import BaseTemplateService, MakoTemplateService

    binder.bind(BaseTemplateService, to=MakoTemplateService(), scope=singleton)
