import sys
from typing import Final

from loguru import logger

LOGGER_FORMAT: Final[str] = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"  # noqa: E501
)


def configure_logging(debug: bool) -> None:
    if not debug:
        return
    logger.enable("adrpy")
    logger.remove()
    logger.add(sys.stderr, format=LOGGER_FORMAT, level="DEBUG", filter="adrpy")
