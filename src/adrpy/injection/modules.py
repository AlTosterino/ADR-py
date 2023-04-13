from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.settings import Settings
from injector import Module, provider, singleton


class RepositoryModules(Module):
    @singleton
    @provider
    def provide_adr_repository(self, settings: Settings) -> BaseADRRepository:
        from adrpy.repositories.adr.repository import ADRFileRepository

        return ADRFileRepository(settings=settings)


class ServiceModules(Module):
    @singleton
    @provider
    def provide_template_service(self) -> BaseTemplateService:
        from adrpy.services.template.service import MakoTemplateService

        return MakoTemplateService()
