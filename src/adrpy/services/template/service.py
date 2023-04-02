from mako.template import Template as MakoTemplate

from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.value_objects.template import FileTemplate, RenderedTemplate


class MakoTemplateService(BaseTemplateService):
    def render(self, template: FileTemplate, data: dict) -> RenderedTemplate:
        mako_template = MakoTemplate(template.content)
        mako_render = mako_template.render(**data)
        return RenderedTemplate(path=template.path, content=mako_render)
