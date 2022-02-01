"""Test the utils module in example."""

from src.example.util import rando


def test_rando() -> None:
    assert rando() == 4
