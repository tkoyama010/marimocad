"""Unit tests for marimocad operations (transformations and boolean ops)."""

import pytest

import marimocad as mc


class TestTransformations:
    """Test transformation operations."""

    def test_translate(self) -> None:
        """Test translation operation."""
        box = mc.box(10, 10, 10)
        moved = mc.translate(box, x=5, y=10, z=2)
        assert moved is not None

    def test_translate_no_offset(self) -> None:
        """Test translation with no offset."""
        box = mc.box(10, 10, 10)
        same = mc.translate(box)
        assert same is not None

    def test_rotate_z_axis(self) -> None:
        """Test rotation around Z axis."""
        box = mc.box(10, 10, 10)
        rotated = mc.rotate(box, 45, axis="Z")
        assert rotated is not None

    def test_rotate_x_axis(self) -> None:
        """Test rotation around X axis."""
        box = mc.box(10, 10, 10)
        rotated = mc.rotate(box, 90, axis="X")
        assert rotated is not None

    def test_rotate_y_axis(self) -> None:
        """Test rotation around Y axis."""
        box = mc.box(10, 10, 10)
        rotated = mc.rotate(box, 180, axis="Y")
        assert rotated is not None

    def test_rotate_custom_axis(self) -> None:
        """Test rotation around custom axis."""
        box = mc.box(10, 10, 10)
        rotated = mc.rotate(box, 45, axis=(1, 1, 0))
        assert rotated is not None

    def test_rotate_with_center(self) -> None:
        """Test rotation with custom center."""
        box = mc.box(10, 10, 10)
        rotated = mc.rotate(box, 45, axis="Z", center=(5, 5, 5))
        assert rotated is not None

    def test_rotate_invalid_axis(self) -> None:
        """Test rotation with invalid axis string."""
        box = mc.box(10, 10, 10)
        with pytest.raises(ValueError, match="Invalid axis string"):
            mc.rotate(box, 45, axis="W")

    def test_scale_uniform(self) -> None:
        """Test uniform scaling."""
        box = mc.box(10, 10, 10)
        bigger = mc.scale(box, 2.0)
        assert bigger is not None

    def test_scale_non_uniform(self) -> None:
        """Test non-uniform scaling."""
        box = mc.box(10, 10, 10)
        stretched = mc.scale(box, (1, 2, 0.5))
        assert stretched is not None

    def test_scale_with_center(self) -> None:
        """Test scaling with custom center."""
        box = mc.box(10, 10, 10)
        scaled = mc.scale(box, 2.0, center=(5, 5, 5))
        assert scaled is not None

    def test_mirror_xy_plane(self) -> None:
        """Test mirroring across XY plane."""
        box = mc.box(10, 10, 10)
        mirrored = mc.mirror(box, plane="XY")
        assert mirrored is not None

    def test_mirror_yz_plane(self) -> None:
        """Test mirroring across YZ plane."""
        box = mc.box(10, 10, 10)
        mirrored = mc.mirror(box, plane="YZ")
        assert mirrored is not None

    def test_mirror_xz_plane(self) -> None:
        """Test mirroring across XZ plane."""
        box = mc.box(10, 10, 10)
        mirrored = mc.mirror(box, plane="XZ")
        assert mirrored is not None

    def test_mirror_custom_plane(self) -> None:
        """Test mirroring across custom plane."""
        box = mc.box(10, 10, 10)
        mirrored = mc.mirror(box, plane=(1, 0, 0))
        assert mirrored is not None

    def test_mirror_invalid_plane(self) -> None:
        """Test mirroring with invalid plane string."""
        box = mc.box(10, 10, 10)
        with pytest.raises(ValueError, match="Invalid plane string"):
            mc.mirror(box, plane="AB")


class TestBooleanOperations:
    """Test boolean operations."""

    def test_union_two_boxes(self) -> None:
        """Test union of two boxes."""
        box1 = mc.box(10, 10, 10)
        box2 = mc.translate(mc.box(10, 10, 10), x=5)
        combined = mc.union(box1, box2)
        assert combined is not None

    def test_union_single_geometry(self) -> None:
        """Test union with single geometry."""
        box = mc.box(10, 10, 10)
        result = mc.union(box)
        assert result is not None

    def test_union_multiple_geometries(self) -> None:
        """Test union of multiple geometries."""
        box1 = mc.box(10, 10, 10)
        box2 = mc.translate(mc.box(10, 10, 10), x=5)
        box3 = mc.translate(mc.box(10, 10, 10), y=5)
        combined = mc.union(box1, box2, box3)
        assert combined is not None

    def test_union_no_geometries(self) -> None:
        """Test union with no geometries raises error."""
        with pytest.raises(ValueError, match="At least one geometry"):
            mc.union()

    def test_subtract_box_from_box(self) -> None:
        """Test subtracting box from box."""
        box = mc.box(20, 20, 10)
        hole = mc.cylinder(3, 15)
        result = mc.subtract(box, hole)
        assert result is not None

    def test_subtract_no_tools(self) -> None:
        """Test subtract with no tools returns base."""
        box = mc.box(10, 10, 10)
        result = mc.subtract(box)
        assert result is not None

    def test_subtract_multiple_tools(self) -> None:
        """Test subtracting multiple tools."""
        box = mc.box(20, 20, 10)
        hole1 = mc.cylinder(2, 15)
        hole2 = mc.translate(mc.cylinder(2, 15), x=5)
        result = mc.subtract(box, hole1, hole2)
        assert result is not None

    def test_intersect_box_sphere(self) -> None:
        """Test intersection of box and sphere."""
        box = mc.box(10, 10, 10)
        sphere = mc.sphere(6)
        result = mc.intersect(box, sphere)
        assert result is not None

    def test_intersect_single_geometry(self) -> None:
        """Test intersect with single geometry."""
        box = mc.box(10, 10, 10)
        result = mc.intersect(box)
        assert result is not None

    def test_intersect_multiple_geometries(self) -> None:
        """Test intersection of multiple geometries."""
        box1 = mc.box(10, 10, 10)
        box2 = mc.translate(mc.box(10, 10, 10), x=5)
        sphere = mc.sphere(6)
        result = mc.intersect(box1, box2, sphere)
        assert result is not None

    def test_intersect_no_geometries(self) -> None:
        """Test intersect with no geometries raises error."""
        with pytest.raises(ValueError, match="At least one geometry"):
            mc.intersect()


class TestComplexOperations:
    """Test complex combinations of operations."""

    def test_translate_and_rotate(self) -> None:
        """Test combining translation and rotation."""
        box = mc.box(10, 10, 10)
        moved = mc.translate(box, x=5)
        rotated = mc.rotate(moved, 45, axis="Z")
        assert rotated is not None

    def test_scale_and_mirror(self) -> None:
        """Test combining scaling and mirroring."""
        box = mc.box(10, 10, 10)
        scaled = mc.scale(box, 2.0)
        mirrored = mc.mirror(scaled, plane="XY")
        assert mirrored is not None

    def test_union_with_transformations(self) -> None:
        """Test union with transformed geometries."""
        box1 = mc.box(10, 10, 10)
        box2 = mc.rotate(mc.translate(mc.box(10, 10, 10), x=5), 45, axis="Z")
        combined = mc.union(box1, box2)
        assert combined is not None
