from abc import ABC, abstractmethod

from adrpy.shared_kernel.value_objects.template import File, RenderedFile


class BaseTemplateService(ABC):
    @abstractmethod
    def render(self, template_file: File, data: dict) -> RenderedFile:
        ...
