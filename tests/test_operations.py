"""Tests for advanced operations."""

import cadquery as cq
import pytest

from marimocad.operations import extrude, revolve, sweep
from marimocad.sketch import Sketch


class TestExtrude:
    """Tests for extrude operation."""

    def test_extrude_from_sketch(self):
        """Test extrude from Sketch object."""
        sketch = Sketch().circle(10)
        result = extrude(sketch, 20)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) >= 1

    def test_extrude_from_workplane(self):
        """Test extrude from Workplane."""
        wp = cq.Workplane("XY").rect(10, 10)
        result = extrude(wp, 15)
        assert isinstance(result, cq.Workplane)

    def test_extrude_both_directions(self):
        """Test extrude in both directions."""
        sketch = Sketch().rectangle(10, 10)
        result = extrude(sketch, 10, both=True)
        assert isinstance(result, cq.Workplane)

    def test_extrude_zero_distance(self):
        """Test that zero distance raises ValueError."""
        sketch = Sketch().circle(5)
        with pytest.raises(ValueError, match="cannot be zero"):
            extrude(sketch, 0)

    def test_extrude_invalid_profile(self):
        """Test that invalid profile raises TypeError."""
        with pytest.raises(TypeError, match="must be a Workplane or Sketch"):
            extrude("not a profile", 10)

    def test_extrude_rectangle(self):
        """Test extruding a rectangle."""
        sketch = Sketch().rectangle(20, 10)
        result = extrude(sketch, 30)
        assert isinstance(result, cq.Workplane)


class TestRevolve:
    """Tests for revolve operation."""

    def test_revolve_full(self):
        """Test full 360 degree revolve."""
        sketch = Sketch().rectangle(10, 20, centered=False)
        result = revolve(sketch, angle=360)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) >= 1

    def test_revolve_partial(self):
        """Test partial revolve."""
        sketch = Sketch().rectangle(5, 10, centered=False)
        result = revolve(sketch, angle=180)
        assert isinstance(result, cq.Workplane)

    def test_revolve_from_workplane(self):
        """Test revolve from Workplane."""
        wp = cq.Workplane("XY").moveTo(5, 0).rect(3, 10)
        result = revolve(wp, angle=360)
        assert isinstance(result, cq.Workplane)

    def test_revolve_custom_axis(self):
        """Test revolve with custom axis."""
        sketch = Sketch("XZ").rectangle(5, 10, centered=False)
        result = revolve(sketch, angle=180, axis=(0, 1, 0))
        assert isinstance(result, cq.Workplane)

    def test_revolve_zero_angle(self):
        """Test that zero angle raises ValueError."""
        sketch = Sketch().rectangle(5, 10)
        with pytest.raises(ValueError, match="cannot be zero"):
            revolve(sketch, angle=0)

    def test_revolve_zero_axis(self):
        """Test that zero axis raises ValueError."""
        sketch = Sketch().rectangle(5, 10)
        with pytest.raises(ValueError, match="cannot be the zero vector"):
            revolve(sketch, angle=180, axis=(0, 0, 0))

    def test_revolve_invalid_profile(self):
        """Test that invalid profile raises TypeError."""
        with pytest.raises(TypeError, match="must be a Workplane or Sketch"):
            revolve("not a profile", angle=180)


class TestSweep:
    """Tests for sweep operation."""

    def test_sweep_basic(self):
        """Test basic sweep operation."""
        profile = Sketch().circle(2)
        # Create a proper path with consolidated wire
        path = cq.Workplane("XZ").moveTo(0, 0).lineTo(10, 0).lineTo(20, 5).consolidateWires()
        result = sweep(profile, path)
        assert isinstance(result, cq.Workplane)

    def test_sweep_from_workplane(self):
        """Test sweep with Workplane profile."""
        profile = cq.Workplane("XY").circle(3)
        path = cq.Workplane("XZ").moveTo(0, 0).lineTo(15, 0).lineTo(30, 10).consolidateWires()
        result = sweep(profile, path)
        assert isinstance(result, cq.Workplane)

    def test_sweep_invalid_profile(self):
        """Test that invalid profile raises TypeError."""
        path = cq.Workplane("XZ").lineTo(10, 0)
        with pytest.raises(TypeError, match="must be a Workplane or Sketch"):
            sweep("not a profile", path)

    def test_sweep_invalid_path(self):
        """Test that invalid path raises TypeError."""
        profile = Sketch().circle(2)
        with pytest.raises(TypeError, match="must be a Workplane or Wire"):
            sweep(profile, "not a path")

    def test_sweep_path_no_wires(self):
        """Test that path with no wires raises ValueError."""
        profile = Sketch().circle(2)
        path = cq.Workplane("XY")  # Empty workplane
        with pytest.raises(ValueError, match="contains no wires"):
            sweep(profile, path)

    def test_sweep_rectangle_profile(self):
        """Test sweep with rectangle profile."""
        profile = Sketch().rectangle(4, 4)
        path = cq.Workplane("XZ").moveTo(0, 0).lineTo(10, 0).lineTo(20, 0).consolidateWires()
        result = sweep(profile, path)
        assert isinstance(result, cq.Workplane)
