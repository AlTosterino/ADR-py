from abc import ABC, abstractmethod

from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template

# TODO: Add example how to use adrpy with custom DatabaseRepository

class BaseADRRepository(ABC):
    @abstractmethod
    def get_template(self, name: str) -> Template:  # TODO: Rename to get_app_template
        ...

    @abstractmethod
    def create(self, adr_name: str, template: RenderedTemplate) -> None:
        ...


# ? Possibility of custom templates?
