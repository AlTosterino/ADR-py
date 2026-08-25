from adrpy.injection.container import lidi
from adrpy.injection.modules import bind_modules
from adrpy.injection.settings import bind_settings


def setup_injection() -> None:
    bind_settings(lidi)
    bind_modules(lidi)
