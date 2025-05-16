from abc import ABC, abstractmethod

from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template


class ITemplateService(ABC):
    @abstractmethod
    def render(self, template_file: Template, data: dict) -> RenderedTemplate: ...
