"""Tests for main module imports."""



class TestImports:
    """Test that all main exports are available."""

    def test_import_primitives(self):
        """Test importing primitive functions."""
        from marimocad import box, cone, cylinder, sphere, torus

        assert callable(box)
        assert callable(sphere)
        assert callable(cylinder)
        assert callable(cone)
        assert callable(torus)

    def test_import_transforms(self):
        """Test importing transform functions."""
        from marimocad import rotate, scale, translate

        assert callable(translate)
        assert callable(rotate)
        assert callable(scale)

    def test_import_boolean(self):
        """Test importing boolean functions."""
        from marimocad import difference, intersection, union

        assert callable(union)
        assert callable(difference)
        assert callable(intersection)

    def test_import_sketch(self):
        """Test importing Sketch class."""
        from marimocad import Sketch

        assert Sketch is not None

    def test_import_operations(self):
        """Test importing operation functions."""
        from marimocad import extrude, revolve, sweep

        assert callable(extrude)
        assert callable(revolve)
        assert callable(sweep)

    def test_version(self):
        """Test that version is defined."""
        import marimocad

        assert hasattr(marimocad, "__version__")
        assert marimocad.__version__ == "0.1.0"

    def test_all_exports(self):
        """Test that __all__ is defined correctly."""
        import marimocad

        assert hasattr(marimocad, "__all__")
        expected = [
            "box",
            "sphere",
            "cylinder",
            "cone",
            "torus",
            "translate",
            "rotate",
            "scale",
            "union",
            "difference",
            "intersection",
            "Sketch",
            "extrude",
            "revolve",
            "sweep",
        ]
        for item in expected:
            assert item in marimocad.__all__


class TestIntegration:
    """Integration tests combining multiple operations."""

    def test_create_and_transform_box(self):
        """Test creating and transforming a box."""
        from marimocad import box, rotate, translate

        box_wp = box(10, 10, 10)
        moved = translate(box_wp, x=5)
        rotated = rotate(moved, axis=(0, 0, 1), angle=45)
        assert rotated is not None

    def test_boolean_operations(self):
        """Test boolean operations on primitives."""
        from marimocad import box, cylinder, difference

        box_wp = box(20, 20, 20)
        hole = cylinder(5, 25)
        result = difference(box_wp, hole)
        assert result is not None

    def test_sketch_and_extrude(self):
        """Test creating a sketch and extruding it."""
        from marimocad import Sketch, extrude

        sketch = Sketch().circle(10)
        extruded = extrude(sketch, 20)
        assert extruded is not None

    def test_sketch_and_revolve(self):
        """Test creating a sketch and revolving it."""
        from marimocad import Sketch, revolve

        sketch = Sketch().rectangle(10, 20, centered=False)
        revolved = revolve(sketch, angle=360)
        assert revolved is not None
