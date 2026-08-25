from lidipy import Lidi

from adrpy.shared_kernel.settings import Settings


def bind_settings(lidi: Lidi) -> None:
    lidi.bind(Settings, Settings(), singleton=True)
