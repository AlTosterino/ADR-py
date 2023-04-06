from pathlib import Path

from adrpy.services.file.base import BaseFileService
from adrpy.shared_kernel.value_objects.template import File


class FileService(BaseFileService):
    def get_file(self, path: Path) -> File:
        with open(path, "r") as file:
            content = file.read()
        return File(path=path, content=content)

    def create_file(self, path: Path, filename: str, content: str) -> None:
        file_path = path / filename
        with open(file_path, "w") as file:
            file.write(content)
