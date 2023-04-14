from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.value_objects.template import RenderedTemplate, Template
from mako.template import Template as MakoTemplate


class MakoTemplateService(BaseTemplateService):
    def render(self, template_file: Template, data: dict) -> RenderedTemplate:
        mako_template = MakoTemplate(template_file.content)
        mako_render = mako_template.render(**data)
        return RenderedTemplate(name=template_file.name, content=mako_render)
