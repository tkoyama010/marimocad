"""Tests for primitive shape creation."""

import cadquery as cq
import pytest

from marimocad.primitives import box, cone, cylinder, sphere, torus


class TestBox:
    """Tests for box primitive."""

    def test_box_basic(self):
        """Test basic box creation."""
        result = box(10, 20, 30)
        assert isinstance(result, cq.Workplane)
        # Check that we have a solid
        solids = result.solids().vals()
        assert len(solids) == 1

    def test_box_centered(self):
        """Test centered box."""
        result = box(10, 10, 10, centered=True)
        assert isinstance(result, cq.Workplane)

    def test_box_not_centered(self):
        """Test non-centered box."""
        result = box(10, 10, 10, centered=False)
        assert isinstance(result, cq.Workplane)

    def test_box_invalid_dimensions(self):
        """Test that invalid dimensions raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            box(0, 10, 10)
        with pytest.raises(ValueError, match="must be positive"):
            box(10, -5, 10)
        with pytest.raises(ValueError, match="must be positive"):
            box(10, 10, 0)


class TestSphere:
    """Tests for sphere primitive."""

    def test_sphere_basic(self):
        """Test basic sphere creation."""
        result = sphere(10)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) == 1

    def test_sphere_with_angles(self):
        """Test sphere with custom angles."""
        result = sphere(5, angle1=0, angle2=90)
        assert isinstance(result, cq.Workplane)

    def test_sphere_invalid_radius(self):
        """Test that invalid radius raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            sphere(0)
        with pytest.raises(ValueError, match="must be positive"):
            sphere(-5)


class TestCylinder:
    """Tests for cylinder primitive."""

    def test_cylinder_basic(self):
        """Test basic cylinder creation."""
        result = cylinder(5, 10)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) == 1

    def test_cylinder_not_centered(self):
        """Test non-centered cylinder."""
        result = cylinder(5, 10, centered=False)
        assert isinstance(result, cq.Workplane)

    def test_cylinder_partial(self):
        """Test partial cylinder with angle."""
        result = cylinder(5, 10, angle=180)
        assert isinstance(result, cq.Workplane)

    def test_cylinder_invalid_params(self):
        """Test that invalid parameters raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            cylinder(0, 10)
        with pytest.raises(ValueError, match="must be positive"):
            cylinder(5, -10)


class TestCone:
    """Tests for cone primitive."""

    def test_cone_basic(self):
        """Test basic cone creation."""
        result = cone(10, 0, 20)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) == 1

    def test_cone_frustum(self):
        """Test frustum (truncated cone)."""
        result = cone(10, 5, 15)
        assert isinstance(result, cq.Workplane)

    def test_cone_invalid_params(self):
        """Test that invalid parameters raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            cone(-1, 0, 10)
        with pytest.raises(ValueError, match="must be positive"):
            cone(10, 5, 0)
        with pytest.raises(ValueError, match="At least one radius"):
            cone(0, 0, 10)


class TestTorus:
    """Tests for torus primitive."""

    def test_torus_basic(self):
        """Test basic torus creation."""
        result = torus(20, 5)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) == 1

    def test_torus_partial(self):
        """Test partial torus."""
        result = torus(15, 3, angle1=0, angle2=180)
        assert isinstance(result, cq.Workplane)

    def test_torus_invalid_params(self):
        """Test that invalid parameters raise ValueError."""
        with pytest.raises(ValueError, match="Major radius must be positive"):
            torus(0, 5)
        with pytest.raises(ValueError, match="Minor radius must be positive"):
            torus(20, 0)
