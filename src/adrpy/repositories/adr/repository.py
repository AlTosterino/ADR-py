from pathlib import Path
from typing import Final

from adrpy.injection import Inject
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template


class ADRFileRepository(BaseADRRepository):
    APP_TEMPLATES_DIR: Final[Path] = (
        Path(__file__).parents[1] / "templates"
    )  # TODO: Move to settings

    def __init__(self, settings: Inject[Settings]) -> None:
        self.settings = settings

    def get_template(self, name: str) -> Template:
        template_path = self.APP_TEMPLATES_DIR / name
        with open(template_path, "r") as file:
            content = file.read()
        return Template(name=name, content=content)

    def create(self, adr_name: str, rendered_template: RenderedTemplate) -> None:
        self.settings.adr_dir.mkdir(parents=True, exist_ok=True)
        with open(
            self.settings.adr_dir / self.__get_filename_with_extension(name=adr_name), "w"
        ) as file:
            file.write(rendered_template.content)

    def __get_filename_with_extension(self, name: str) -> str:
        return f"{name}.md"
