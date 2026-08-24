import re

import yaml

from adrpy.services.metadata.base import IMetadataService
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.value_objects.adr import AdrMetadata


class YamlMetadataService(IMetadataService):
    FRONT_MATTER_PATTERN = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)

    def render_front_matter(self, metadata: AdrMetadata) -> str:
        body = yaml.safe_dump(
            metadata.to_mapping(), allow_unicode=True, default_flow_style=False, sort_keys=False
        ).rstrip()
        return f"---\n{body}\n---"

    def parse_document(self, content: str) -> AdrMetadata:
        match = self.FRONT_MATTER_PATTERN.match(content)
        if match is None:
            raise MetadataValidationError("ADR document must start with YAML front matter")
        try:
            data = yaml.safe_load(match.group("body"))
        except yaml.YAMLError as error:
            raise MetadataValidationError("ADR front matter is not valid YAML") from error
        return AdrMetadata.from_mapping(data)
