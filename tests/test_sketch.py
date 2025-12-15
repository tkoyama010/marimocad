"""Tests for Sketch class."""

import pytest
import cadquery as cq
from marimocad.sketch import Sketch


class TestSketchInit:
    """Tests for Sketch initialization."""

    def test_sketch_default_plane(self):
        """Test sketch with default XY plane."""
        sketch = Sketch()
        assert sketch._plane == "XY"

    def test_sketch_xy_plane(self):
        """Test sketch with XY plane."""
        sketch = Sketch("XY")
        assert sketch._plane == "XY"

    def test_sketch_xz_plane(self):
        """Test sketch with XZ plane."""
        sketch = Sketch("XZ")
        assert sketch._plane == "XZ"

    def test_sketch_yz_plane(self):
        """Test sketch with YZ plane."""
        sketch = Sketch("YZ")
        assert sketch._plane == "YZ"

    def test_sketch_invalid_plane(self):
        """Test that invalid plane raises ValueError."""
        with pytest.raises(ValueError, match="must be one of"):
            Sketch("XYZ")


class TestSketchRectangle:
    """Tests for rectangle method."""

    def test_rectangle_basic(self):
        """Test basic rectangle."""
        sketch = Sketch().rectangle(10, 20)
        wp = sketch.get_workplane()
        assert isinstance(wp, cq.Workplane)

    def test_rectangle_not_centered(self):
        """Test non-centered rectangle."""
        sketch = Sketch().rectangle(10, 20, centered=False)
        assert isinstance(sketch, Sketch)

    def test_rectangle_invalid_dimensions(self):
        """Test that invalid dimensions raise ValueError."""
        sketch = Sketch()
        with pytest.raises(ValueError, match="must be positive"):
            sketch.rectangle(0, 10)
        with pytest.raises(ValueError, match="must be positive"):
            sketch.rectangle(10, -5)

    def test_rectangle_chaining(self):
        """Test method chaining."""
        sketch = Sketch().rectangle(10, 10)
        assert isinstance(sketch, Sketch)


class TestSketchCircle:
    """Tests for circle method."""

    def test_circle_basic(self):
        """Test basic circle."""
        sketch = Sketch().circle(10)
        wp = sketch.get_workplane()
        assert isinstance(wp, cq.Workplane)

    def test_circle_invalid_radius(self):
        """Test that invalid radius raises ValueError."""
        sketch = Sketch()
        with pytest.raises(ValueError, match="must be positive"):
            sketch.circle(0)
        with pytest.raises(ValueError, match="must be positive"):
            sketch.circle(-5)

    def test_circle_chaining(self):
        """Test method chaining."""
        sketch = Sketch().circle(5)
        assert isinstance(sketch, Sketch)


class TestSketchPolygon:
    """Tests for polygon method."""

    def test_polygon_triangle(self):
        """Test triangle (3-sided polygon)."""
        sketch = Sketch().polygon(3, 10)
        assert isinstance(sketch, Sketch)

    def test_polygon_hexagon(self):
        """Test hexagon (6-sided polygon)."""
        sketch = Sketch().polygon(6, 20)
        assert isinstance(sketch, Sketch)

    def test_polygon_invalid_sides(self):
        """Test that invalid number of sides raises ValueError."""
        sketch = Sketch()
        with pytest.raises(ValueError, match="at least 3 sides"):
            sketch.polygon(2, 10)

    def test_polygon_invalid_diameter(self):
        """Test that invalid diameter raises ValueError."""
        sketch = Sketch()
        with pytest.raises(ValueError, match="must be positive"):
            sketch.polygon(5, 0)


class TestSketchLines:
    """Tests for line drawing methods."""

    def test_line(self):
        """Test line method."""
        sketch = Sketch().line(10, 5)
        assert isinstance(sketch, Sketch)

    def test_line_to(self):
        """Test line_to method."""
        sketch = Sketch().line_to(10, 10)
        assert isinstance(sketch, Sketch)

    def test_move_to(self):
        """Test move_to method."""
        sketch = Sketch().move_to(5, 5)
        assert isinstance(sketch, Sketch)

    def test_close(self):
        """Test close method."""
        sketch = Sketch().line(10, 0).line(0, 10).line(-10, 0).close()
        assert isinstance(sketch, Sketch)


class TestSketchArc:
    """Tests for arc method."""

    def test_arc_basic(self):
        """Test basic arc."""
        sketch = Sketch().arc((10, 10), 5)
        assert isinstance(sketch, Sketch)

    def test_arc_invalid_radius(self):
        """Test that invalid radius raises ValueError."""
        sketch = Sketch()
        with pytest.raises(ValueError, match="must be positive"):
            sketch.arc((10, 10), 0)


class TestSketchComplex:
    """Tests for complex sketch operations."""

    def test_multiple_shapes(self):
        """Test sketch with multiple shapes."""
        sketch = Sketch().circle(10).rectangle(20, 20)
        wp = sketch.get_workplane()
        assert isinstance(wp, cq.Workplane)

    def test_complex_path(self):
        """Test complex path with lines and arcs."""
        sketch = Sketch()
        sketch.move_to(0, 0)
        sketch.line(10, 0)
        sketch.line(0, 10)
        sketch.line(-10, 0)
        sketch.close()
        assert isinstance(sketch, Sketch)

    def test_get_workplane(self):
        """Test get_workplane method."""
        sketch = Sketch().circle(10)
        wp = sketch.get_workplane()
        assert isinstance(wp, cq.Workplane)

    def test_repr(self):
        """Test string representation."""
        sketch = Sketch("XY")
        assert "XY" in repr(sketch)
