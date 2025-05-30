from pathlib import Path
from typing import Annotated, Any

import typer

from adrpy.injection import lidi
from adrpy.shared_kernel.dtos import CreateAdrDto, InitializeAdrDto
from adrpy.shared_kernel.logging import configure_logging
from adrpy.shared_kernel.settings import Settings
from adrpy.use_cases.create import CreateAdr
from adrpy.use_cases.initialize import InitializeAdr

app = typer.Typer()


def set_settings(**kwargs: Any) -> None:
    """
    Set settings for the application.
    This function is called before any command is executed.
    """
    configure_logging(debug=kwargs.pop("debug", False))
    settings = Settings(**kwargs)
    lidi.bind(Settings, settings, singleton=True)


@app.command()
def init(
    path: Path | None = typer.Argument(
        None,
        help=(
            "Path in where ADRs should reside. "
            "If not provided, Path will be extracted from pyproject.toml.  "
            "If no pyproject.toml is found, ADRs will be initialized in the current "
            "working directory."
        ),
    ),
    debug: Annotated[
        bool,
        typer.Option(help="Enable debug logs"),
    ] = False,
) -> None:
    """
    Initialize ADR directory with first ADR in given PATH
    """
    settings: dict[str, Any] = {"debug": debug}
    if path:
        settings["initial_adr_dir"] = path
    set_settings(**settings)
    dto = InitializeAdrDto(path=path)
    InitializeAdr.execute(dto=dto)


@app.command()
def new(
    name: Annotated[
        str,
        typer.Argument(
            help="Name of new ADR. Longer names (with spaces) should be put in quotation marks."
        ),
    ],
    debug: Annotated[
        bool,
        typer.Option(help="Enable debug logs"),
    ] = False,
) -> None:
    """
    Create new ADR with given NAME
    """
    set_settings(debug=debug)
    dto = CreateAdrDto(name=name)
    CreateAdr.execute(dto=dto)


def cli_entrypoint() -> None:
    app()
