from pathlib import Path

import typer

from adrpy.services.template.service import MakoTemplateService

app = typer.Typer()


@app.command()
def init(path: Path) -> None:
    service = MakoTemplateService()
    file_template = service.get_template("initial-adr")
    rendered_template = service.render(file_template, {"date": "TODAY", "status": "ACCEPTED"})
    print(rendered_template)


@app.command()
def other(path: Path) -> None:
    pass


def cli_entrypoint() -> None:
    app()
