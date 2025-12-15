"""Basic tests for marimocad package."""

import marimocad


def test_version() -> None:
    """Test that version is defined."""
    assert hasattr(marimocad, "__version__")
    assert isinstance(marimocad.__version__, str)
    assert marimocad.__version__ == "0.1.0"
