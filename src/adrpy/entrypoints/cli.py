from pathlib import Path
from typing import Annotated

import typer

from adrpy.injection import lidi
from adrpy.shared_kernel.dtos import CreateAdrDto, InitializeAdrDto
from adrpy.shared_kernel.settings import Settings
from adrpy.use_cases.create import CreateAdr
from adrpy.use_cases.initialize import InitializeAdr

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
    config: Annotated[
        Path | None,
        typer.Option("--config", help="TOML configuration file used to resolve the ADR directory."),
    ] = None,
) -> None:
    """
    Initialize ADR directory with first ADR in given PATH
    """
    if path:
        new_settings = Settings(initial_adr_dir=path, config_path=config)
        lidi.bind(Settings, new_settings, singleton=True)
    elif config:
        new_settings = Settings(config_path=config)
        lidi.bind(Settings, new_settings, singleton=True)
    dto = InitializeAdrDto(path=path, config_path=config)
    InitializeAdr.execute(dto=dto)


@app.command()
def new(
    name: Annotated[
        str,
        typer.Argument(
            help="Name of new ADR. Longer names (with spaces) should be put in quotation marks."
        ),
    ],
    config: Annotated[
        Path | None,
        typer.Option("--config", help="TOML configuration file used to resolve the ADR directory."),
    ] = None,
) -> None:
    """
    Create new ADR with given NAME
    """
    if config:
        lidi.bind(Settings, Settings(config_path=config), singleton=True)
    dto = CreateAdrDto(name=name, config_path=config)
    CreateAdr.execute(dto=dto)


def cli_entrypoint() -> None:
    app()
