"""Utilities for noclist"""

from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger
from sys import stderr


def get_logger() -> Logger:
    logger = getLogger()
    logger.setLevel(DEBUG)
    handler = StreamHandler(stderr)
    handler.setLevel(DEBUG)
    formatter = Formatter("DEBUG: %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
