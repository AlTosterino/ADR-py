from adrpy.shared_kernel.settings import Settings
from lidipy import Lidi


def bind_settings(lidi: Lidi) -> None:
    lidi.bind(Settings, Settings(), singleton=True)
