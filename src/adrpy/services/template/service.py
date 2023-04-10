from adrpy.services.template.base import BaseTemplateService
from adrpy.shared_kernel.value_objects.template import File, RenderedFile
from mako.template import Template as MakoTemplate


class MakoTemplateService(BaseTemplateService):
    def render(self, template_file: File, data: dict) -> RenderedFile:
        mako_template = MakoTemplate(template_file.content)
        mako_render = mako_template.render(**data)
        return RenderedFile(path=template_file.path, content=mako_render)
