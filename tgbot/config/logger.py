import logging
import sys

from loguru import logger

from config import settings


def init_logging() -> None:
    # ----- LOGGING -----
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )

    # ----- LOGURU -----
    logger.remove()
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(
        sink=sys.stderr,
        format=logger_format,
        colorize=settings.DEBUG
    )
