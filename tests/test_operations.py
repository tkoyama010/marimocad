"""Tests for operations module."""

import pytest
from marimocad import Box, Sphere, Cylinder, union, intersection, difference


def test_union_two_shapes():
    """Test union of two shapes."""
    box1 = Box(width=10, height=10, depth=10)
    box2 = Box(width=5, height=5, depth=5)
    
    result = union(box1, box2)
    assert len(result.shapes) == 2


def test_union_multiple_shapes():
    """Test union of multiple shapes."""
    box = Box(width=5, height=5, depth=5)
    sphere = Sphere(radius=3)
    cylinder = Cylinder(radius=2, height=10)
    
    result = union(box, sphere, cylinder)
    assert len(result.shapes) == 3


def test_union_requires_multiple_shapes():
    """Test that union requires at least 2 shapes."""
    box = Box(width=5, height=5, depth=5)
    
    with pytest.raises(ValueError):
        union(box)


def test_intersection_two_shapes():
    """Test intersection of two shapes."""
    box = Box(width=10, height=10, depth=10)
    sphere = Sphere(radius=6)
    
    result = intersection(box, sphere)
    assert len(result.shapes) == 2


def test_difference_two_shapes():
    """Test difference of two shapes."""
    box = Box(width=10, height=10, depth=10)
    sphere = Sphere(radius=5)
    
    result = difference(box, sphere)
    assert result.base == box
    assert sphere in result.to_subtract


def test_difference_multiple_shapes():
    """Test difference with multiple shapes to subtract."""
    box = Box(width=10, height=10, depth=10)
    sphere1 = Sphere(radius=3)
    sphere2 = Sphere(radius=2)
    
    result = difference(box, sphere1, sphere2)
    assert result.base == box
    assert len(result.to_subtract) == 2


def test_difference_requires_shapes_to_subtract():
    """Test that difference requires shapes to subtract."""
    box = Box(width=10, height=10, depth=10)
    
    with pytest.raises(ValueError):
        difference(box)


def test_operation_with_name():
    """Test that operations can be named."""
    box = Box(width=5, height=5, depth=5)
    sphere = Sphere(radius=3)
    
    result = union(box, sphere, name="my_union")
    assert result.name == "my_union"
