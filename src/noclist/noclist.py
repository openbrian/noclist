"""The Foo module provides things and functions."""

from __future__ import annotations

from hashlib import sha256


class Noclist:
    """The Noclist class calls the adhoc/noclist server."""

    @staticmethod
    def authenticate() -> bool:
        return True

    @staticmethod
    def build_checksum(auth_token: str, request_path: str) -> str:
        target: bytes = str.encode(f"{auth_token}{request_path}")
        return sha256(target).hexdigest()
