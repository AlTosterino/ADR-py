from pathlib import Path

from adrpy.shared_kernel.settings import Settings
from injector import Binder, singleton


def configure_settings(binder: Binder) -> None:
    settings = Settings(working_directory=Path.cwd())
    binder.bind(Settings, to=settings, scope=singleton)
