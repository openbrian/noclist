"""The main entry point into this package when run as a script."""

# For more details, see also
# https://docs.python.org/3/library/runpy.html
# https://docs.python.org/3/reference/import.html#special-considerations-for-main

import os
import sys

from src.example.example import Example


def main() -> None:
    """Execute the Something standalone command-line tool."""
    _ = Example.do_something()


def init() -> None:
    if __name__ == "__main__":
        main()
        sys.exit(os.EX_OK)


init()
