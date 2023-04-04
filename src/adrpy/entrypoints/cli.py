from pathlib import Path

import typer

from adrpy.injection import Inject, injector
from adrpy.services.template.service import BaseTemplateService, MakoTemplateService

app = typer.Typer()


def test_inject(template_service: Inject[BaseTemplateService]) -> None:
    print(template_service)


class TestInject:
    def __init__(self, template_service: Inject[BaseTemplateService]):
        self.template_service = template_service


@app.command()
def init(path: Path) -> None:
    test_callable = injector.get(BaseTemplateService)
    print(test_callable)
    test_class = injector.get(TestInject)
    print(test_class.template_service)
    # Dynamic binding?
    injector.binder.bind(BaseTemplateService, to=object())
    test_class = injector.get(TestInject)
    print(test_class.template_service)
    service = MakoTemplateService()
    file_template = service.get_template("initial-adr")
    rendered_template = service.render(file_template, {"date": "TODAY", "status": "ACCEPTED"})
    print(rendered_template)


@app.command()
def other(path: Path) -> None:
    pass


def cli_entrypoint() -> None:
    app()
