import logging
from rich.logging import RichHandler


def logger_factory(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    rich_handler = RichHandler(level=logging.INFO)
    formater = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
    rich_handler.setFormatter(formater)
    logger.addHandler(rich_handler)
    return logger
