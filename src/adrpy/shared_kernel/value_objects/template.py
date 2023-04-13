from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    name: str
    content: str


@dataclass(frozen=True)
class RenderedTemplate(Template):
    pass
