"""The Foo module provides things and functions."""

from hashlib import sha256
from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger
from sys import stderr
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

NOCHOST: str = "http://localhost:8888"


class Noclist:
    """The Noclist class calls the adhoc/noclist server."""

    @staticmethod
    def authenticate() -> Optional[str]:
        """Returns the token."""
        url: str = f"{NOCHOST}/auth"
        request = Request(url)
        try:
            # urlopen will handle redirects
            with urlopen(request) as response:
                # This lookup is case-insensitive.  If this header is not
                # present None is returned.
                return str(response.headers["badsec-authentication-token"])
        # BCD: Even though I mock out an HTTPError side_effect, urlopen will
        # raise a URLError!
        # except HTTPError as error:
        #     logger = get_logger()
        #     logger.debug('auth 1 httperror')
        #     logger.debug(error)
        #     return None
        except URLError as error:
            logger: Logger = get_logger()
            logger.debug("auth 2 urlerror")
            logger.debug(error)
            return None

    @staticmethod
    def build_checksum(auth_token: str, request_path: str) -> str:
        target: bytes = str.encode(f"{auth_token}{request_path}")
        return sha256(target).hexdigest()


def get_logger() -> Logger:
    logger = getLogger()
    logger.setLevel(DEBUG)
    handler = StreamHandler(stderr)
    handler.setLevel(DEBUG)
    formatter = Formatter("DEBUG: %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
