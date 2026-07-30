"""Pytest configuration and fixtures for marimocad tests."""

from pathlib import Path

import pytest


@pytest.fixture(params=sorted(Path("examples").glob("*.py")))
def filepath(request):
    """Parametrized fixture providing example file paths.

    This fixture automatically discovers all Python files in the examples
    directory and provides them to tests that request it.
    """
    return request.param
