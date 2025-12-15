"""Tests for transformation operations."""

import pytest
import numpy as np
from marimocad import Box, Cylinder, Sphere, translate, rotate, scale
from marimocad.transforms import mirror


def test_translate_box():
    """Test translating a box."""
    box = Box(width=5, height=5, depth=5)
    translate(box, x=10, y=5, z=3)
    
    np.testing.assert_array_equal(box.position, [10, 5, 3])


def test_translate_incremental():
    """Test incremental translations."""
    cylinder = Cylinder(radius=2, height=8)
    
    translate(cylinder, x=5)
    np.testing.assert_array_equal(cylinder.position, [5, 0, 0])
    
    translate(cylinder, y=3)
    np.testing.assert_array_equal(cylinder.position, [5, 3, 0])
    
    translate(cylinder, z=-2)
    np.testing.assert_array_equal(cylinder.position, [5, 3, -2])


def test_rotate_box():
    """Test rotating a box."""
    box = Box(width=10, height=3, depth=3)
    rotate(box, angle=45, axis='z')
    
    assert hasattr(box, '_rotations')
    assert len(box._rotations) == 1
    assert box._rotations[0]['angle'] == 45
    assert box._rotations[0]['axis'] == (0, 0, 1)


def test_rotate_custom_axis():
    """Test rotating around a custom axis."""
    cylinder = Cylinder(radius=3, height=10)
    rotate(cylinder, angle=90, axis=(1, 1, 0))
    
    assert hasattr(cylinder, '_rotations')
    assert box._rotations[0]['axis'] == (1, 1, 0)


def test_scale_uniform():
    """Test uniform scaling."""
    sphere = Sphere(radius=3)
    original_radius = sphere.radius
    
    scale(sphere, factor=2.0)
    assert sphere.radius == original_radius * 2


def test_scale_non_uniform_box():
    """Test non-uniform scaling on a box."""
    box = Box(width=5, height=5, depth=5)
    
    scale(box, x=2, y=1, z=0.5)
    
    assert box.width == 10
    assert box.height == 5
    assert box.depth == 2.5


def test_scale_invalid_factor():
    """Test that negative scale factors raise ValueError."""
    box = Box(width=5, height=5, depth=5)
    
    with pytest.raises(ValueError):
        scale(box, factor=-1)
    
    with pytest.raises(ValueError):
        scale(box, x=-2)


def test_mirror_xy():
    """Test mirroring across XY plane."""
    box = Box(width=5, height=5, depth=5)
    translate(box, z=10)
    
    mirror(box, plane='xy')
    assert box.position[2] == -10


def test_mirror_xz():
    """Test mirroring across XZ plane."""
    box = Box(width=5, height=5, depth=5)
    translate(box, y=10)
    
    mirror(box, plane='xz')
    assert box.position[1] == -10


def test_mirror_yz():
    """Test mirroring across YZ plane."""
    box = Box(width=5, height=5, depth=5)
    translate(box, x=10)
    
    mirror(box, plane='yz')
    assert box.position[0] == -10


def test_mirror_invalid_plane():
    """Test that invalid plane raises ValueError."""
    box = Box(width=5, height=5, depth=5)
    
    with pytest.raises(ValueError):
        mirror(box, plane='invalid')


def test_transform_chaining():
    """Test that transformations can be chained."""
    cylinder = Cylinder(radius=2, height=10)
    
    translate(cylinder, x=5, y=5, z=0)
    rotate(cylinder, angle=45, axis='z')
    scale(cylinder, factor=1.5)
    
    np.testing.assert_array_almost_equal(cylinder.position, [7.5, 7.5, 0])
    assert cylinder.radius == 3.0
    assert cylinder.height == 15.0
