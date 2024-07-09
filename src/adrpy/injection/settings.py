from lidipy import Lidi


def bind_settings(lidi: Lidi) -> None:
    from adrpy.shared_kernel.settings import Settings

    lidi.bind(Settings, Settings(), singleton=True)
