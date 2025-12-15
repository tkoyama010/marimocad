"""Tests for boolean operations."""

import cadquery as cq
import pytest

from marimocad.boolean import difference, intersection, union
from marimocad.primitives import box, cylinder, sphere
from marimocad.transforms import translate


class TestUnion:
    """Tests for union operation."""

    def test_union_two_boxes(self):
        """Test union of two boxes."""
        box1 = box(10, 10, 10)
        box2 = translate(box(10, 10, 10), x=5)
        result = union(box1, box2)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) >= 1

    def test_union_multiple(self):
        """Test union of multiple shapes."""
        box1 = box(10, 10, 10)
        box2 = translate(box(5, 5, 5), x=10)
        box3 = translate(box(5, 5, 5), y=10)
        result = union(box1, box2, box3)
        assert isinstance(result, cq.Workplane)

    def test_union_sphere_box(self):
        """Test union of sphere and box."""
        sphere_wp = sphere(10)
        box_wp = box(15, 15, 15)
        result = union(sphere_wp, box_wp)
        assert isinstance(result, cq.Workplane)

    def test_union_insufficient_args(self):
        """Test that union with < 2 args raises ValueError."""
        box1 = box(10, 10, 10)
        with pytest.raises(ValueError, match="at least 2 workplanes"):
            union(box1)

    def test_union_invalid_input(self):
        """Test that invalid input raises TypeError."""
        box1 = box(10, 10, 10)
        with pytest.raises(TypeError, match="must be CadQuery Workplanes"):
            union(box1, "not a workplane")


class TestDifference:
    """Tests for difference operation."""

    def test_difference_basic(self):
        """Test basic difference operation."""
        box_wp = box(20, 20, 20)
        hole = cylinder(5, 25)
        result = difference(box_wp, hole)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) >= 1

    def test_difference_multiple_tools(self):
        """Test difference with multiple tools."""
        box_wp = box(30, 30, 30)
        hole1 = cylinder(5, 35)
        hole2 = translate(cylinder(5, 35), x=10)
        result = difference(box_wp, hole1, hole2)
        assert isinstance(result, cq.Workplane)

    def test_difference_sphere_from_box(self):
        """Test subtracting sphere from box."""
        box_wp = box(20, 20, 20)
        sphere_wp = sphere(12)
        result = difference(box_wp, sphere_wp)
        assert isinstance(result, cq.Workplane)

    def test_difference_no_tools(self):
        """Test that difference with no tools raises ValueError."""
        box_wp = box(10, 10, 10)
        with pytest.raises(ValueError, match="at least one tool"):
            difference(box_wp)

    def test_difference_invalid_base(self):
        """Test that invalid base raises TypeError."""
        hole = cylinder(5, 10)
        with pytest.raises(TypeError, match="Base must be"):
            difference("not a workplane", hole)

    def test_difference_invalid_tool(self):
        """Test that invalid tool raises TypeError."""
        box_wp = box(10, 10, 10)
        with pytest.raises(TypeError, match="must be CadQuery Workplanes"):
            difference(box_wp, "not a workplane")


class TestIntersection:
    """Tests for intersection operation."""

    def test_intersection_two_boxes(self):
        """Test intersection of two boxes."""
        box1 = box(20, 20, 20)
        box2 = translate(box(20, 20, 20), x=10)
        result = intersection(box1, box2)
        assert isinstance(result, cq.Workplane)
        solids = result.solids().vals()
        assert len(solids) >= 1

    def test_intersection_multiple(self):
        """Test intersection of multiple shapes."""
        box1 = box(20, 20, 20)
        box2 = translate(box(20, 20, 20), x=5)
        box3 = translate(box(20, 20, 20), y=5)
        result = intersection(box1, box2, box3)
        assert isinstance(result, cq.Workplane)

    def test_intersection_sphere_box(self):
        """Test intersection of sphere and box."""
        sphere_wp = sphere(15)
        box_wp = box(20, 20, 20)
        result = intersection(sphere_wp, box_wp)
        assert isinstance(result, cq.Workplane)

    def test_intersection_insufficient_args(self):
        """Test that intersection with < 2 args raises ValueError."""
        box1 = box(10, 10, 10)
        with pytest.raises(ValueError, match="at least 2 workplanes"):
            intersection(box1)

    def test_intersection_invalid_input(self):
        """Test that invalid input raises TypeError."""
        box1 = box(10, 10, 10)
        with pytest.raises(TypeError, match="must be CadQuery Workplanes"):
            intersection(box1, "not a workplane")
