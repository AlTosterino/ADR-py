from pathlib import Path
from typing import Annotated

import typer

from adrpy.injection import lidi
from adrpy.shared_kernel.dtos import CreateAdrDto, InitializeAdrDto
from adrpy.shared_kernel.errors import MetadataValidationError
from adrpy.shared_kernel.settings import Settings
from adrpy.shared_kernel.value_objects.adr import normalize_tags, validate_status
from adrpy.use_cases.create import CreateAdr
from adrpy.use_cases.initialize import InitializeAdr

app = typer.Typer()


def _creation_metadata(status: str, tags: list[str] | None) -> tuple[str, tuple[str, ...]]:
    try:
        return validate_status(status), normalize_tags(tags or ())
    except MetadataValidationError as error:
        raise typer.BadParameter(str(error)) from error


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
    validated_status, validated_tags = _creation_metadata(status, tags)
    dto = InitializeAdrDto(
        path=path,
        config_path=config,
        status=validated_status,
        tags=validated_tags,
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
    validated_status, validated_tags = _creation_metadata(status, tags)
    dto = CreateAdrDto(
        name=name,
        config_path=config,
        status=validated_status,
        tags=validated_tags,
    )
    CreateAdr.execute(dto=dto)


def cli_entrypoint() -> None:
    app()
