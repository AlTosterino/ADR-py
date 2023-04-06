from enum import Enum
from pathlib import Path
from typing import Final

APP_TEMPLATES_DIR: Final[Path] = Path(__file__).parents[2] / "templates"


class AppTemplatePaths(Enum):
    INITIAL_ADR = APP_TEMPLATES_DIR / "initial_adr.md"
