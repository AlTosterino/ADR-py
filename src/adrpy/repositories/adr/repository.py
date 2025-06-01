from typing import Final

from adrpy.injection import lidi
from adrpy.repositories.adr.base import IADRRepository
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template


class ADRFileRepository(IADRRepository):
    SETTINGS: Final[Settings] = lidi.resolve_attr(Settings)

    def get_template(self, name: str) -> Template:
        # TODO: Move `get_template` to `ITemplateService` or create persistence repository/facade
        template_path = self.SETTINGS.APP_TEMPLATES_DIR / name
        with open(template_path, "r") as file:
            content = file.read()
        return Template(name=name, content=content)

    def create(self, adr_name: str, template: RenderedTemplate) -> None:
        self.SETTINGS.adr_dir.mkdir(parents=True, exist_ok=True)
        new_adr_path = self.SETTINGS.adr_dir / self.__get_filename_with_extension(name=adr_name)
        with open(new_adr_path, "w") as file:
            file.write(template.content)

    def get_next_ordinal_number(self) -> int:
        ordinal_number = 0
        for path in self.SETTINGS.adr_dir.glob("*.md"):
            # TODO: Use front matter (metadata) to store ordinal number
            filename = path.stem
            parts = filename.split("-", 1)
            if not parts or not parts[0].isdigit():
                continue
            prefix_as_int = int(parts[0])
            ordinal_number = max(ordinal_number, prefix_as_int)
        return ordinal_number + 1

    @staticmethod
    def __get_filename_with_extension(name: str) -> str:
        return f"{name}.md"
