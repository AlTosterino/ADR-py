import frontmatter
from yaml import YAMLError

from adrpy.services.metadata.base import IMetadataService
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class YamlMetadataService(IMetadataService):
    def render_front_matter(self, metadata: AdrMetadata) -> str:
        post = frontmatter.Post(content="", **metadata.to_mapping())
        return frontmatter.dumps(post)

    def parse_document(self, content: str) -> AdrMetadata:
        try:
            data = frontmatter.loads(content).metadata
        except YAMLError as error:
            raise MetadataValidationError("ADR front matter is not valid YAML") from error
        return AdrMetadata.from_mapping(data)
