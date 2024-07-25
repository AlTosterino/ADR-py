from pathlib import Path
from typing import Annotated

import typer
from adrpy.injection import lidi
from adrpy.shared_kernel.dtos import CreateADRDTO, InitializeADRDTO
from adrpy.shared_kernel.settings import Settings
from adrpy.use_cases.creating import CreatingADR
from adrpy.use_cases.initializing import InitializingADR

app = typer.Typer()


@app.command()
def init(
    path: Path = typer.Argument(
        None,
        help=(
            "Path in where ADRs should reside. "
            "If not provided, Path will be extracted from pyproject.toml.  "
            "If no pyproject.toml is found, ADRs will be initialized in the current "
            "working directory."
        ),
    ),
) -> None:
    """
    Initialize ADR directory with first ADR in given PATH
    """
    if path:
        new_settings = Settings(initial_adr_dir=path)
        lidi.bind(Settings, new_settings, singleton=True)
    dto = InitializeADRDTO(path=path)
    InitializingADR().execute(dto=dto)


@app.command()
def new(
    name: Annotated[
        str,
        typer.Argument(
            help="Name of new ADR. Longer names (with spaces) should be put in quotation marks."
        ),
    ]
) -> None:
    """
    Create new ADR with given NAME
    """
    dto = CreateADRDTO(name=name)
    CreatingADR().execute(dto=dto)


def cli_entrypoint() -> None:
    app()
