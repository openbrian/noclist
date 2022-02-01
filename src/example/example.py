"""The Foo module provides things and functions."""


# pylint: disable=too-few-public-methods
class Example:
    """The Foo class provides sample methods."""

    @staticmethod
    def do_something(value: bool = False) -> bool:
        """Return true, always."""
        return value or True
