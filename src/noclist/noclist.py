"""The Foo module provides things and functions."""

from hashlib import sha256
from logging import Logger
from typing import List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

from src.noclist.utils import get_logger

NOCHOST: str = "http://localhost:8888"


class Noclist:
    """The Noclist class calls the adhoc/noclist server."""

    @staticmethod
    def authenticate(timeout: float) -> Optional[str]:
        """Returns the token."""
        url: str = f"{NOCHOST}/auth"
        request = Request(url)
        try:
            # urlopen will handle redirects
            with urlopen(request, timeout=timeout) as response:
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
            logger.debug("There was an issue connecting to %s.", url)
            logger.debug(error)
            return None

    @staticmethod
    def build_checksum(auth_token: str, request_path: str) -> str:
        target: bytes = str.encode(f"{auth_token}{request_path}")
        return sha256(target).hexdigest()

    @staticmethod
    def get_users(checksum: str, timeout: float) -> List[str]:
        url: str = f"{NOCHOST}/users"
        headers: dict[str, str] = {"X-Request-Checksum": checksum}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=timeout) as response:
            data: str = response.read().decode("UTF-8")
        return data.split("\n")
