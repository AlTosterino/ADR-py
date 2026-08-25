from pathlib import Path
from typing import Annotated

import typer

from adrpy.injection import lidi
from adrpy.shared_kernel.dtos import CreateAdrDto, InitializeAdrDto
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.adr import AdrCreationMetadata
from adrpy.use_cases.create import CreateAdr
from adrpy.use_cases.initialize import InitializeAdr
from adrpy.use_cases.list_adrs import ListAdrs

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
    status: Annotated[
        str,
        typer.Option("--status", help="Initial ADR status.", show_default=True),
    ] = "proposed",
    tags: Annotated[
        list[str] | None,
        typer.Option("--tag", help="ADR tag; repeat this option to add multiple tags."),
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
    creation_metadata = _creation_metadata(status, tags)
    dto = InitializeAdrDto(
        path=path,
        config_path=config,
        status=creation_metadata.status,
        tags=creation_metadata.tags,
    )
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
    status: Annotated[
        str,
        typer.Option("--status", help="Initial ADR status.", show_default=True),
    ] = "proposed",
    tags: Annotated[
        list[str] | None,
        typer.Option("--tag", help="ADR tag; repeat this option to add multiple tags."),
    ] = None,
) -> None:
    """
    Create new ADR with given NAME
    """
    if config:
        lidi.bind(Settings, Settings(config_path=config), singleton=True)
    creation_metadata = _creation_metadata(status, tags)
    dto = CreateAdrDto(
        name=name,
        config_path=config,
        status=creation_metadata.status,
        tags=creation_metadata.tags,
    )
    CreateAdr.execute(dto=dto)


@app.command(name="list")
def list_adrs(
    path: Path = typer.Argument(
        None,
        help="Directory containing ADR Markdown files; defaults to configured ADR directory.",
    ),
    config: Annotated[
        Path | None,
        typer.Option("--config", help="TOML configuration file used to resolve the ADR directory."),
    ] = None,
) -> None:
    """List ADRs with their status, tags, and superseded state."""
    if path:
        lidi.bind(Settings, Settings(initial_adr_dir=path, config_path=config), singleton=True)
    elif config:
        lidi.bind(Settings, Settings(config_path=config), singleton=True)

    try:
        items = ListAdrs.execute()
    except MetadataValidationError as error:
        raise typer.BadParameter(str(error)) from error

    if not items:
        typer.echo("No ADRs found.")
        return

    typer.echo(
        "ORDINAL  TITLE                                      STATUS       "
        "TAGS                 SUPERSEDED  FILE"
    )
    typer.echo(
        "-------  ----------------------------------------  -----------  "
        "-------------------  ----------  ------------------------------"
    )
    for item in items:
        tags = ", ".join(item.tags) or "-"
        superseded = "yes" if item.is_superseded else "no"
        typer.echo(
            f"{item.ordinal:04d}  {item.title[:40]:40}  {item.status:11}  "
            f"{tags[:19]:19}  {superseded:10}  {item.filename}"
        )


def cli_entrypoint() -> None:
    app()


def _creation_metadata(status: str, tags: list[str] | None) -> AdrCreationMetadata:
    try:
        return AdrCreationMetadata(status=status, tags=tuple(tags or ()))
    except MetadataValidationError as error:
        raise typer.BadParameter(str(error)) from error
