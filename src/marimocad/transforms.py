"""Transformation operations for shapes.

This module provides functions for transforming shapes through translation,
rotation, and scaling operations.

Examples:
    Translate a shape::

        from marimocad import Box, translate
        box = Box(width=5, height=5, depth=5)
        moved_box = translate(box, x=10, y=5, z=0)

    Rotate a shape::

        from marimocad import Cylinder, rotate
        cylinder = Cylinder(radius=2, height=10)
        rotated = rotate(cylinder, angle=45, axis='z')

    Scale a shape::

        from marimocad import Sphere, scale
        sphere = Sphere(radius=5)
        scaled = scale(sphere, factor=2.0)
"""

from typing import Union, Tuple
import numpy as np
from .shapes import Shape


def translate(
    shape: Shape,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
) -> Shape:
    """Translate (move) a shape by the specified distances.
    
    Args:
        shape: The shape to translate.
        x: Distance to move along the x-axis.
        y: Distance to move along the y-axis.
        z: Distance to move along the z-axis.
    
    Returns:
        The translated shape (same object, modified in place).
    
    Examples:
        Move a box to a new position::
        
            box = Box(width=10, height=5, depth=3)
            translate(box, x=10, y=5, z=2)
            print(box.position)  # [10, 5, 2]
        
        Move multiple steps::
        
            cylinder = Cylinder(radius=3, height=10)
            translate(cylinder, x=5)
            translate(cylinder, y=3, z=-2)
    """
    shape.position += np.array([x, y, z])
    return shape


def rotate(
    shape: Shape,
    angle: float,
    axis: Union[str, Tuple[float, float, float]] = 'z',
) -> Shape:
    """Rotate a shape around an axis.
    
    Note: This is a placeholder implementation that stores rotation intent.
    Full 3D rotation would require more complex geometry handling.
    
    Args:
        shape: The shape to rotate.
        angle: Rotation angle in degrees.
        axis: Either 'x', 'y', 'z' or a custom (x, y, z) axis vector.
    
    Returns:
        The shape (rotation metadata stored).
    
    Examples:
        Rotate around z-axis::
        
            box = Box(width=10, height=5, depth=3)
            rotate(box, angle=45, axis='z')
        
        Rotate around custom axis::
        
            cylinder = Cylinder(radius=3, height=10)
            rotate(cylinder, angle=90, axis=(1, 1, 0))
    """
    # Store rotation information in the shape
    if not hasattr(shape, '_rotations'):
        shape._rotations = []
    
    if isinstance(axis, str):
        axis_map = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
        axis_vector = axis_map.get(axis.lower(), (0, 0, 1))
    else:
        axis_vector = axis
    
    shape._rotations.append({
        'angle': angle,
        'axis': axis_vector,
    })
    
    return shape


def scale(
    shape: Shape,
    factor: float = 1.0,
    x: float = None,
    y: float = None,
    z: float = None,
) -> Shape:
    """Scale a shape uniformly or non-uniformly.
    
    Args:
        shape: The shape to scale.
        factor: Uniform scale factor (used if x, y, z not specified).
        x: Scale factor along x-axis (overrides factor).
        y: Scale factor along y-axis (overrides factor).
        z: Scale factor along z-axis (overrides factor).
    
    Returns:
        The scaled shape (same object, modified in place).
    
    Raises:
        ValueError: If scale factors are not positive.
    
    Examples:
        Uniform scaling::
        
            box = Box(width=5, height=5, depth=5)
            scale(box, factor=2.0)  # All dimensions doubled
        
        Non-uniform scaling::
        
            cylinder = Cylinder(radius=3, height=10)
            scale(cylinder, x=2, y=2, z=1)  # Radius doubled, height same
    """
    # Determine scale factors
    sx = x if x is not None else factor
    sy = y if y is not None else factor
    sz = z if z is not None else factor
    
    if sx <= 0 or sy <= 0 or sz <= 0:
        raise ValueError("Scale factors must be positive")
    
    # Apply scaling based on shape type
    from .shapes import Box, Cylinder, Sphere
    
    if isinstance(shape, Box):
        shape.width *= sx
        shape.height *= sy
        shape.depth *= sz
    elif isinstance(shape, Cylinder):
        shape.radius *= (sx + sy) / 2  # Average for radius
        shape.height *= sz
    elif isinstance(shape, Sphere):
        # Uniform scaling for sphere
        avg_scale = (sx + sy + sz) / 3
        shape.radius *= avg_scale
    
    # Scale position as well
    shape.position *= np.array([sx, sy, sz])
    
    return shape


def mirror(shape: Shape, plane: str = 'xy') -> Shape:
    """Mirror a shape across a plane.
    
    Args:
        shape: The shape to mirror.
        plane: The plane to mirror across ('xy', 'xz', or 'yz').
    
    Returns:
        The mirrored shape (same object, modified in place).
    
    Examples:
        Mirror across XY plane::
        
            box = Box(width=5, height=5, depth=5)
            translate(box, z=10)
            mirror(box, plane='xy')  # Now at z=-10
    """
    plane = plane.lower()
    
    if plane == 'xy':
        shape.position[2] *= -1
    elif plane == 'xz':
        shape.position[1] *= -1
    elif plane == 'yz':
        shape.position[0] *= -1
    else:
        raise ValueError(f"Invalid plane: {plane}. Use 'xy', 'xz', or 'yz'")
    
    return shape
