"""Common configuration for pytest."""

import os

import pytest


@pytest.fixture(scope="module")
def timeout() -> float:
    """in seconds"""
    return float(os.getenv("NOCLIST_TIMEOUT", "2.0"))
