"""Tests for transformation operations."""

import pytest
import cadquery as cq
from marimocad.primitives import box, sphere
from marimocad.transforms import translate, rotate, scale


class TestTranslate:
    """Tests for translate operation."""

    def test_translate_basic(self):
        """Test basic translation."""
        box_wp = box(10, 10, 10)
        result = translate(box_wp, x=5, y=10, z=15)
        assert isinstance(result, cq.Workplane)

    def test_translate_single_axis(self):
        """Test translation along a single axis."""
        box_wp = box(10, 10, 10)
        result = translate(box_wp, x=20)
        assert isinstance(result, cq.Workplane)

    def test_translate_no_offset(self):
        """Test translation with no offset."""
        box_wp = box(10, 10, 10)
        result = translate(box_wp)
        assert isinstance(result, cq.Workplane)

    def test_translate_invalid_input(self):
        """Test that invalid input raises TypeError."""
        with pytest.raises(TypeError, match="must be a CadQuery Workplane"):
            translate("not a workplane", x=5)


class TestRotate:
    """Tests for rotate operation."""

    def test_rotate_z_axis(self):
        """Test rotation around Z axis."""
        box_wp = box(10, 10, 10)
        result = rotate(box_wp, axis=(0, 0, 1), angle=45)
        assert isinstance(result, cq.Workplane)

    def test_rotate_x_axis(self):
        """Test rotation around X axis."""
        box_wp = box(10, 10, 10)
        result = rotate(box_wp, axis=(1, 0, 0), angle=90)
        assert isinstance(result, cq.Workplane)

    def test_rotate_y_axis(self):
        """Test rotation around Y axis."""
        box_wp = box(10, 10, 10)
        result = rotate(box_wp, axis=(0, 1, 0), angle=180)
        assert isinstance(result, cq.Workplane)

    def test_rotate_with_center(self):
        """Test rotation around a custom center point."""
        box_wp = box(10, 10, 10)
        result = rotate(box_wp, axis=(0, 0, 1), angle=45, center=(5, 5, 5))
        assert isinstance(result, cq.Workplane)

    def test_rotate_zero_axis(self):
        """Test that zero axis raises ValueError."""
        box_wp = box(10, 10, 10)
        with pytest.raises(ValueError, match="cannot be the zero vector"):
            rotate(box_wp, axis=(0, 0, 0), angle=45)

    def test_rotate_invalid_input(self):
        """Test that invalid input raises TypeError."""
        with pytest.raises(TypeError, match="must be a CadQuery Workplane"):
            rotate("not a workplane", axis=(0, 0, 1), angle=45)


class TestScale:
    """Tests for scale operation."""

    def test_scale_uniform(self):
        """Test uniform scaling."""
        box_wp = box(10, 10, 10)
        result = scale(box_wp, x=2, y=2, z=2)
        assert isinstance(result, cq.Workplane)

    def test_scale_non_uniform(self):
        """Test non-uniform scaling."""
        box_wp = box(10, 10, 10)
        result = scale(box_wp, x=2, y=1, z=0.5)
        assert isinstance(result, cq.Workplane)

    def test_scale_single_axis(self):
        """Test scaling along a single axis."""
        box_wp = box(10, 10, 10)
        result = scale(box_wp, x=3)
        assert isinstance(result, cq.Workplane)

    def test_scale_no_change(self):
        """Test scaling with factor of 1."""
        box_wp = box(10, 10, 10)
        result = scale(box_wp)
        assert isinstance(result, cq.Workplane)

    def test_scale_invalid_factors(self):
        """Test that invalid scale factors raise ValueError."""
        box_wp = box(10, 10, 10)
        with pytest.raises(ValueError, match="must be positive"):
            scale(box_wp, x=0)
        with pytest.raises(ValueError, match="must be positive"):
            scale(box_wp, y=-1)

    def test_scale_invalid_input(self):
        """Test that invalid input raises TypeError."""
        with pytest.raises(TypeError, match="must be a CadQuery Workplane"):
            scale("not a workplane", x=2)

    def test_scale_sphere(self):
        """Test scaling a sphere."""
        sphere_wp = sphere(10)
        result = scale(sphere_wp, x=2, y=2, z=2)
        assert isinstance(result, cq.Workplane)
