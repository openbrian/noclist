"""The Noclist module is a collection of functions.  There's no state stored in the class ."""

from hashlib import sha256
from logging import Logger
from typing import List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

from src.noclist.utils import get_logger

LOG: Logger = get_logger()
nochost_default: str = "http://localhost:8888"


class Noclist:
    """The Noclist class calls the adhoc/noclist server."""

    # Candidate assumptions, constants
    UID_MIN_LENGTH: int = 5
    UID_MAX_LENGTH: int = 20
    ATTEMPT_MAX_NUM: int = 3

    @staticmethod
    def authenticate(nochost: str, timeout: float) -> Optional[str]:
        """Returns the authentication token."""
        # Candidate: Even though I mock out an HTTPError side_effect, urlopen will
        # raise a URLError!
        request = Request(url=f"{nochost}/auth")
        [token, _] = Noclist._call_api(Noclist.ATTEMPT_MAX_NUM, request, timeout)
        if len(token) == 0:  # Assume an empty token is not a valid token
            return None
        return token

    @staticmethod
    def _call_api(
        attempt_number: int, request: Request, timeout: float
    ) -> tuple[str, str]:
        """Recursively tries to call the API.  Will fail if attempt_number is 0.
        Returns tuple of the:
           * badsec-authentication-token or ""
           * http body or "".
        This method does not handle any business logic of Noclist aside from
        trying multiple times to call the API.
        Returning ("", "") means the call failed.
        """
        LOG.debug("_call_api attempt %s", attempt_number)
        if attempt_number == 0:
            return "", ""
        try:
            # urlopen will handle redirects
            with urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    LOG.debug("Auth response code was not 200")
                    return Noclist._call_api(attempt_number - 1, request, timeout)
                # This lookup is case-insensitive.  If this header is not
                # present None is returned.
                token: str = str(response.headers["badsec-authentication-token"])
                data: str = response.read().decode("UTF-8")
                LOG.debug("token %s", token)
                LOG.debug("data %s", data)
                return token, data
        except URLError as error:
            LOG.debug("There was an issue connecting to the API.")
            LOG.debug(error)
            return Noclist._call_api(attempt_number - 1, request, timeout)

    @staticmethod
    def build_checksum(auth_token: str, request_path: str) -> str:
        target: bytes = str.encode(f"{auth_token}{request_path}")
        return sha256(target).hexdigest()

    @staticmethod
    def get_users(nochost: str, checksum: str, timeout: float) -> List[str]:
        """Return list of valid users."""
        request = Request(
            url=f"{nochost}/users", headers={"X-Request-Checksum": checksum}
        )
        [_, data] = Noclist._call_api(Noclist.ATTEMPT_MAX_NUM, request, timeout)
        if len(data) == 0:
            return []
        uids: list[str] = data.split("\n")
        return [uid for uid in uids if Noclist.is_valid_uid(uid)]

    @staticmethod
    def is_valid_uid(uid: str) -> bool:
        """This validation is based on empirical evidence from Candidate.  It's
        not specified.  Assume uids are unsigned integers.  2^64 is
        18,446,744,073,709,551,616."""
        if len(uid) < Noclist.UID_MIN_LENGTH:
            return False
        if Noclist.UID_MAX_LENGTH < len(uid):
            return False
        if not uid.isdigit():
            return False
        if pow(2, 64) - 1 < int(uid):
            return False
        return True
