import logging

LOGGER = logging.getLogger(__name__)


def logger_init() -> None:
    LOGGER.setLevel(logging.INFO)
    file_handler = logging.FileHandler("main.log", encoding="utf-8")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
