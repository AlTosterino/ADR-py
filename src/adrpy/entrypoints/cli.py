from pathlib import Path

import typer

from adrpy.injection import injector
from adrpy.shared_kernel.dtos import InitializeADRDTO
from adrpy.use_cases.initializing import InitializingADR

app = typer.Typer()


@app.command()
def init(path: Path) -> None:
    use_case = injector.get(InitializingADR)
    dto = InitializeADRDTO(path=path)
    use_case.execute(dto=dto)


@app.command()
def other(path: Path) -> None:
    pass


def cli_entrypoint() -> None:
    app()
