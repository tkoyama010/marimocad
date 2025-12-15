"""Tests for basic shapes."""

import pytest
import numpy as np
from marimocad import Box, Cylinder, Sphere


def test_box_creation():
    """Test that a box can be created with valid dimensions."""
    box = Box(width=10, height=5, depth=3)
    assert box.width == 10
    assert box.height == 5
    assert box.depth == 3


def test_box_volume():
    """Test box volume calculation."""
    box = Box(width=2, height=3, depth=4)
    assert box.volume() == 24.0


def test_box_surface_area():
    """Test box surface area calculation."""
    box = Box(width=2, height=3, depth=4)
    expected = 2 * (2*3 + 3*4 + 4*2)
    assert box.surface_area() == expected


def test_box_invalid_dimensions():
    """Test that negative dimensions raise ValueError."""
    with pytest.raises(ValueError):
        Box(width=-1, height=5, depth=5)
    
    with pytest.raises(ValueError):
        Box(width=5, height=-1, depth=5)
    
    with pytest.raises(ValueError):
        Box(width=5, height=5, depth=-1)


def test_cylinder_creation():
    """Test that a cylinder can be created."""
    cylinder = Cylinder(radius=3, height=10)
    assert cylinder.radius == 3
    assert cylinder.height == 10


def test_cylinder_volume():
    """Test cylinder volume calculation."""
    cylinder = Cylinder(radius=2, height=5)
    expected = np.pi * 4 * 5
    assert abs(cylinder.volume() - expected) < 1e-10


def test_cylinder_invalid_dimensions():
    """Test that invalid dimensions raise ValueError."""
    with pytest.raises(ValueError):
        Cylinder(radius=-1, height=10)
    
    with pytest.raises(ValueError):
        Cylinder(radius=5, height=-1)


def test_sphere_creation():
    """Test that a sphere can be created."""
    sphere = Sphere(radius=5)
    assert sphere.radius == 5


def test_sphere_volume():
    """Test sphere volume calculation."""
    sphere = Sphere(radius=3)
    expected = (4/3) * np.pi * 27
    assert abs(sphere.volume() - expected) < 1e-10


def test_sphere_surface_area():
    """Test sphere surface area calculation."""
    sphere = Sphere(radius=3)
    expected = 4 * np.pi * 9
    assert abs(sphere.surface_area() - expected) < 1e-10


def test_sphere_invalid_radius():
    """Test that negative radius raises ValueError."""
    with pytest.raises(ValueError):
        Sphere(radius=-1)


def test_shape_names():
    """Test that shapes can be named."""
    box = Box(width=5, height=5, depth=5, name="my_box")
    assert box.name == "my_box"
    
    cylinder = Cylinder(radius=3, height=10, name="my_cylinder")
    assert cylinder.name == "my_cylinder"
    
    sphere = Sphere(radius=5, name="my_sphere")
    assert sphere.name == "my_sphere"


def test_shape_position():
    """Test that shapes have a position attribute."""
    box = Box(width=5, height=5, depth=5)
    assert isinstance(box.position, np.ndarray)
    assert len(box.position) == 3
    np.testing.assert_array_equal(box.position, [0, 0, 0])
