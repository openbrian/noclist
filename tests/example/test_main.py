"""Test the main module in example."""

from pytest import raises
from pytest_mock import MockerFixture

from src.example import __main__
from src.example.__main__ import Example, init, main


def test_main_should_call_example(mocker: MockerFixture) -> None:
    mocked_do_something = mocker.patch.object(Example, "do_something")
    main()
    mocked_do_something.assert_called_once_with()


def test_init_should_call_main(mocker: MockerFixture) -> None:
    mocked_main = mocker.patch.object(__main__, "main")
    mocker.patch.object(__main__, "__name__", "__main__")
    with raises(SystemExit) as pytest_wrapped_e:
        init()
    assert pytest_wrapped_e.type == SystemExit
    mocked_main.assert_called_once_with()
