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
    logger.add(
        sink=sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
        colorize=settings.DEBUG
    )
