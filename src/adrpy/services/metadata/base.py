from abc import ABC, abstractmethod

from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class IMetadataService(ABC):
    @abstractmethod
    def render_front_matter(self, metadata: AdrMetadata) -> str: ...

    @abstractmethod
    def parse_document(self, content: str) -> AdrMetadata: ...
