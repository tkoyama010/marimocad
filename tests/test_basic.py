"""Basic tests for marimocad package."""

import marimocad


def test_version():
    """Test that version is defined."""
    assert hasattr(marimocad, "__version__")
    assert isinstance(marimocad.__version__, str)
    assert len(marimocad.__version__) > 0


def test_package_import():
    """Test that package can be imported."""
    assert marimocad is not None
