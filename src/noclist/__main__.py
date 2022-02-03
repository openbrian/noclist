"""The main entry point into this package when run as a script."""

# For more details, see also
# https://docs.python.org/3/library/runpy.html
# https://docs.python.org/3/reference/import.html#special-considerations-for-main

import json
import os
import sys
from logging import Logger

from src.noclist.noclist import Noclist
from src.noclist.utils import get_logger


def main() -> bool:
    try:
        return run()
    except Exception as exc_info:  # pylint: disable=broad-except
        logger: Logger = get_logger()
        logger.debug("There was an exception.")
        logger.debug(exc_info)
        return False


def run() -> bool:
    """Execute the Something standalone command-line tool."""
    timeout: float = float(os.getenv("NOCLIST_TIMEOUT", "2.0"))  # seconds
    token: str = Noclist.authenticate(timeout)
    if token is not None:
        checksum: str = Noclist.build_checksum(token, "/users")
        users: list[str] = Noclist.get_users(checksum, timeout)
        print(json.dumps(users))
        return True
    return False


def init() -> None:
    if __name__ == "__main__":
        sys.exit(os.EX_OK if main() else os.EX_IOERR)


init()
