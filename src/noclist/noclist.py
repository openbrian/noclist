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

    # BCD assumptions
    UID_MIN_LENGHT: int = 5
    UID_MAX_LENGTH: int = 20

    @staticmethod
    def authenticate(timeout: float) -> Optional[str]:
        """Returns the token."""
        # BCD: Even though I mock out an HTTPError side_effect, urlopen will
        # raise a URLError!
        url: str = f"{NOCHOST}/auth"
        request = Request(url)
        try:
            # urlopen will handle redirects
            with urlopen(request, timeout=timeout) as response:
                # This lookup is case-insensitive.  If this header is not
                # present None is returned.
                return str(response.headers["badsec-authentication-token"])
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
        logger: Logger = get_logger()
        logger.debug(data)
        uids: list[str] = data.split("\n")
        valid_data = [uid for uid in uids if Noclist.is_valid_uid(uid)]
        return valid_data

    @staticmethod
    def is_valid_uid(uid: str) -> bool:
        """This validation is based on empirical evidence from BCD.  It's
        not specified."""
        if len(uid) < Noclist.UID_MIN_LENGHT:
            return False
        if Noclist.UID_MAX_LENGTH < len(uid):
            return False
        if not uid.isdigit():
            return False
        return True
