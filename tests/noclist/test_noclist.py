"""Test the noclist module.  With pytest-mock there's no need for decorator or
context managers."""

from email.message import Message
from urllib.error import HTTPError, URLError

from pytest_mock import MockerFixture

from src.noclist.noclist import Noclist, nochost_default


def test_authenticate(mocker: MockerFixture, timeout: float) -> None:
    # Arrange
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    token: str = "5D51D045-EEFE-A60D-090C-CAF9935400FE"
    context_manager = mocker.MagicMock()
    context_manager.status = 200
    # context_manager.read.return_value = 'http body is irrelevant'
    context_manager.headers.__getitem__.return_value = token  # any header key
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert Noclist.authenticate(nochost_default, timeout) == token


def test_authenticate_bad_status(
    mocker: MockerFixture,
    timeout: float,
) -> None:
    # Arrange
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    context_manager = mocker.MagicMock()
    context_manager.status = 418  # teapot
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert Noclist.authenticate(nochost_default, timeout) is None


def test_authenticate_server_down(
    mocker: MockerFixture,
    timeout: float,
) -> None:
    # Arrange
    message = "The connection refused"
    mocker.patch("urllib.request.urlopen", side_effect=URLError(message))
    # Act and Assert
    assert Noclist.authenticate(nochost_default, timeout) is None


def test_authenticate_http_error(
    mocker: MockerFixture,
    timeout: float,
) -> None:
    # Arrange
    message: Message = Message()
    http_error: HTTPError = HTTPError("url", 42, "msg", message, None)
    mocker.patch("urllib.request.urlopen", side_effect=http_error)
    # Act and Assert
    assert Noclist.authenticate(nochost_default, timeout) is None


def test_build_checksum() -> None:
    # Arrange
    auth_token: str = "12345"
    request_path: str = "/users"
    expected_checksum = (
        "c20acb14a3d3339b9e92daebb173e41379f9f2fad4aa6a6326a696bd90c67419"
    )
    # Act
    hash_: str = Noclist.build_checksum(auth_token, request_path)
    # Assert
    assert hash_ == expected_checksum


def test_get_users(mocker: MockerFixture, timeout: float) -> None:
    # Arrange
    user_list_bytes: bytes = b"333\n12345\n092834098230498230498230984\napple"
    user_list: str = "12345"
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    # token: str = "5D51D045-EEFE-A60D-090C-CAF9935400FE"
    context_manager = mocker.MagicMock()
    context_manager.status = 200
    context_manager.read.return_value = user_list_bytes
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert Noclist.get_users(nochost_default, "checksum", timeout) == [user_list]


def test_get_users_bad_status(mocker: MockerFixture, timeout: float) -> None:
    # Arrange
    mock_urlopen = mocker.patch("src.noclist.noclist.urlopen")
    # token: str = "5D51D045-EEFE-A60D-090C-CAF9935400FE"
    context_manager = mocker.MagicMock()
    context_manager.status = 418  # teapot
    context_manager.__enter__.return_value = context_manager
    mock_urlopen.return_value = context_manager
    # Act and Assert
    assert Noclist.get_users(nochost_default, "checksum", timeout) == []


def test_is_valid_uid() -> None:
    # Arrange
    too_short: str = "333"
    too_long: str = "239872938742983749283749723498273"
    too_big_int: str = str(pow(2, 64))
    non_ints: str = "apple"
    just_right: str = "123456"
    user_list: list[str] = [too_short, too_long, non_ints, too_big_int, just_right]
    # Act
    output = [Noclist.is_valid_uid(uid) for uid in user_list]
    # Assert
    assert output == [False, False, False, False, True]
