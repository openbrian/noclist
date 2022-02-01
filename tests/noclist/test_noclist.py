"""Test the noclist module."""

from src.noclist import noclist


def test_authenticate() -> None:
    assert noclist.Noclist.authenticate() is True


def test_build_checksum() -> None:
    auth_token: str = "12345"
    request_path: str = "/users"
    expected_checksum = (
        "c20acb14a3d3339b9e92daebb173e41379f9f2fad4aa6a6326a696bd90c67419"
    )
    hash_: str = noclist.Noclist.build_checksum(auth_token, request_path)
    assert hash_ == expected_checksum
