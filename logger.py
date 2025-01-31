import logging
from logging.handlers import RotatingFileHandler

from constants import LOGGER_LEVEL

LOGGER = logging.getLogger(__name__)


def logger_init() -> None:
    LOGGER.setLevel(LOGGER_LEVEL)
    file_handler = RotatingFileHandler("main.log", maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
