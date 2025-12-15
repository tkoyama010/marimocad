"""Unit tests for marimocad geometry primitives."""

import pytest

import marimocad as mc


class TestPrimitives3D:
    """Test 3D primitive creation."""

    def test_box_default(self) -> None:
        """Test box creation with default parameters."""
        box = mc.box(10, 20, 5)
        assert box is not None

    def test_box_centered(self) -> None:
        """Test centered box creation."""
        box = mc.box(10, 10, 10, center=True)
        assert box is not None

    def test_sphere_default(self) -> None:
        """Test sphere creation with default parameters."""
        sphere = mc.sphere(5.0)
        assert sphere is not None

    def test_sphere_not_centered(self) -> None:
        """Test sphere creation not centered."""
        sphere = mc.sphere(5.0, center=False)
        assert sphere is not None

    def test_cylinder_default(self) -> None:
        """Test cylinder creation with default parameters."""
        cyl = mc.cylinder(3, 10)
        assert cyl is not None

    def test_cylinder_centered(self) -> None:
        """Test centered cylinder creation."""
        cyl = mc.cylinder(3, 10, center=True)
        assert cyl is not None

    def test_cone_default(self) -> None:
        """Test cone creation with default parameters."""
        cone = mc.cone(5, 10, top_radius=0.1)
        assert cone is not None

    def test_cone_frustum(self) -> None:
        """Test frustum (truncated cone) creation."""
        frustum = mc.cone(5, 10, top_radius=2)
        assert frustum is not None

    def test_cone_centered(self) -> None:
        """Test centered cone creation."""
        cone = mc.cone(5, 10, top_radius=0.1, center=True)
        assert cone is not None

    def test_torus(self) -> None:
        """Test torus creation."""
        torus = mc.torus(10, 2)
        assert torus is not None


class TestPrimitives2D:
    """Test 2D primitive creation."""

    def test_circle(self) -> None:
        """Test circle creation."""
        circle = mc.circle(5)
        assert circle is not None

    def test_rectangle(self) -> None:
        """Test rectangle creation."""
        rect = mc.rectangle(10, 20)
        assert rect is not None

    def test_polygon_triangle(self) -> None:
        """Test polygon creation with triangle."""
        triangle = mc.polygon([(0, 0), (10, 0), (5, 10)])
        assert triangle is not None

    def test_polygon_square(self) -> None:
        """Test polygon creation with square."""
        square = mc.polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        assert square is not None


class TestGeometryValidation:
    """Test validation and error handling."""

    def test_box_positive_dimensions(self) -> None:
        """Test box creation with positive dimensions."""
        box = mc.box(1, 1, 1)
        assert box is not None

    def test_sphere_positive_radius(self) -> None:
        """Test sphere creation with positive radius."""
        sphere = mc.sphere(1.0)
        assert sphere is not None

    def test_cylinder_positive_dimensions(self) -> None:
        """Test cylinder creation with positive dimensions."""
        cyl = mc.cylinder(1, 1)
        assert cyl is not None

    def test_cone_positive_dimensions(self) -> None:
        """Test cone creation with positive dimensions."""
        cone = mc.cone(2, 1, top_radius=0.5)
        assert cone is not None
