from abc import ABC, abstractmethod
from pathlib import Path
from typing import Final

from adrpy.shared_kernel.value_objects.template import FileTemplate, RenderedTemplate


class BaseTemplateService(ABC):
    TEMPLATES_DIR: Final[Path] = Path(__file__).parents[2] / "templates"

    def get_template(self, template_name: str) -> FileTemplate:
        for file in self.TEMPLATES_DIR.glob("*.md"):
            if file.stem == template_name:
                with open(file, "r") as template_file:
                    template_content = template_file.read()
                return FileTemplate(path=file, content=template_content)
        raise Exception("No file!")  # TODO: Change exception

    @abstractmethod
    def render(self, template: FileTemplate, data: dict) -> RenderedTemplate:
        ...
