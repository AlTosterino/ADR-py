from adrpy.shared_kernel.settings import Settings
from injector import Binder, singleton


def configure_settings(binder: Binder) -> None:
    binder.bind(Settings, to=Settings(), scope=singleton)
