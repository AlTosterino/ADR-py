from pathlib import Path
from typing import Final

APP_TEMPLATES_DIR: Final[Path] = Path(__file__).parents[1] / "templates"


class AppTemplatePaths:
    INITIAL_ADR = APP_TEMPLATES_DIR / "initial-adr.md"
    SUPERSEDE_ADR = APP_TEMPLATES_DIR / "supersede-adr.md"
