"""Test the Something module. Add more tests here, as needed."""

# from pytest_mock import mocker

from hypothesis import given, strategies

from src.example import example


@given(strategies.booleans())
def test_do_something(boolean: bool) -> None:
    """An example test."""
    assert example.Example.do_something(boolean) is True
