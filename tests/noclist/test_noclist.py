"""Test the noclist module.  With pytest-mock there's no need for decorator or
context managers."""

from email.message import Message
from urllib.error import HTTPError, URLError

from pytest_mock import MockerFixture

from src.noclist import noclist


def test_authenticate(mocker: MockerFixture) -> None:
    # Arrange
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    token: str = "5D51D045-EEFE-A60D-090C-CAF9935400FE"
    context_manager = mocker.MagicMock()
    # context_manager.getcode.return_value = 200
    # context_manager.read.return_value = 'http body is irrelevant'
    context_manager.headers.__getitem__.return_value = token  # any header key
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert noclist.Noclist.authenticate() == token


def test_authenticate_server_down(mocker: MockerFixture) -> None:
    # Arrange
    message = "The connection refused"
    mocker.patch("urllib.request.urlopen", side_effect=URLError(message))
    # Act and Assert
    assert noclist.Noclist.authenticate() is None


def test_authenticate_http_error(mocker: MockerFixture) -> None:
    # Arrange
    message: Message = Message()
    http_error: HTTPError = HTTPError("url", 42, "msg", message, None)
    mocker.patch("urllib.request.urlopen", side_effect=http_error)
    # Act and Assert
    assert noclist.Noclist.authenticate() is None


def test_build_checksum() -> None:
    # Arrange
    auth_token: str = "12345"
    request_path: str = "/users"
    expected_checksum = (
        "c20acb14a3d3339b9e92daebb173e41379f9f2fad4aa6a6326a696bd90c67419"
    )
    # Act
    hash_: str = noclist.Noclist.build_checksum(auth_token, request_path)
    # Assert
    assert hash_ == expected_checksum


def test_get_users(mocker: MockerFixture) -> None:
    # Arrange
    user_list_bytes: bytes = b"user list"
    user_list: str = "user list"
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    # token: str = "5D51D045-EEFE-A60D-090C-CAF9935400FE"
    context_manager = mocker.MagicMock()
    context_manager.getcode.return_value = 200
    context_manager.read.return_value = user_list_bytes
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert noclist.Noclist.get_users("checksum") == [user_list]
