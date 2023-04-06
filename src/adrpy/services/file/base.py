from abc import ABC, abstractmethod
from pathlib import Path

from adrpy.shared_kernel.value_objects.template import File


class BaseFileService(ABC):
    @abstractmethod
    def get_file(self, path: Path) -> File:
        ...

    @abstractmethod
    def create_file(self, path: Path, filename: str, content: str) -> None:
        ...
