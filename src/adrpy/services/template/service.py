from mako.template import Template as MakoTemplate

from adrpy.services.template.base import ITemplateService
from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template


class MakoTemplateService(ITemplateService):
    def render(self, template_file: Template, data: dict) -> RenderedTemplate:
        mako_template = MakoTemplate(template_file.content)
        mako_render = mako_template.render(**data)
        return RenderedTemplate(name=template_file.name, content=mako_render)
