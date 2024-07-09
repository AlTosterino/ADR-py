import re

from adrpy.injection import lidi
from adrpy.repositories.adr.base import BaseADRRepository
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template


class ADRFileRepository(BaseADRRepository):
    settings = lidi.resolve_attr(Settings)

    def get_template(self, name: str) -> Template:
        template_path = self.settings.APP_TEMPLATES_DIR / name
        with open(template_path, "r") as file:
            content = file.read()
        return Template(name=name, content=content)

    def create(self, adr_name: str, template: RenderedTemplate) -> None:
        self.settings.adr_dir.mkdir(parents=True, exist_ok=True)
        with open(
            self.settings.adr_dir / self.__get_filename_with_extension(name=adr_name), "w"
        ) as file:
            file.write(template.content)

    def get_next_ordinal_number(self) -> int:
        ordinal_number = 0
        for path in self.settings.adr_dir.glob("*.md"):
            filename = path.stem
            maybe_number_prefix = re.findall("\d+", filename)
            if not maybe_number_prefix:
                continue
            if (prefix_as_int := int(maybe_number_prefix[0])) > ordinal_number:
                ordinal_number = prefix_as_int
        return ordinal_number + 1

    @staticmethod
    def __get_filename_with_extension(name: str) -> str:
        return f"{name}.md"
