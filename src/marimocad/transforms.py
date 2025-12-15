"""
Transformation operations for CAD geometries.

This module provides functions to transform geometries through
translation, rotation, and scaling operations.
"""

from typing import Tuple

import cadquery as cq


def translate(
    workplane: cq.Workplane, x: float = 0, y: float = 0, z: float = 0
) -> cq.Workplane:
    """
    Translate (move) a geometry by the specified offset.

    Args:
        workplane: The workplane/geometry to translate
        x: Offset in X direction (default: 0)
        y: Offset in Y direction (default: 0)
        z: Offset in Z direction (default: 0)

    Returns:
        A new Workplane with the translated geometry

    Examples:
        >>> box_wp = box(10, 10, 10)
        >>> moved_box = translate(box_wp, x=20, y=10, z=5)
    """
    if not isinstance(workplane, cq.Workplane):
        raise TypeError("workplane must be a CadQuery Workplane")

    return workplane.translate((x, y, z))


def rotate(
    workplane: cq.Workplane,
    axis: Tuple[float, float, float],
    angle: float,
    center: Tuple[float, float, float] = (0, 0, 0),
) -> cq.Workplane:
    """
    Rotate a geometry around an axis.

    Args:
        workplane: The workplane/geometry to rotate
        axis: Rotation axis as (x, y, z) tuple. E.g., (0, 0, 1) for Z-axis
        angle: Rotation angle in degrees
        center: Center point of rotation as (x, y, z) tuple (default: origin)

    Returns:
        A new Workplane with the rotated geometry

    Raises:
        ValueError: If axis is the zero vector

    Examples:
        >>> box_wp = box(10, 10, 10)
        >>> rotated_box = rotate(box_wp, axis=(0, 0, 1), angle=45)
        >>> rotated_around_point = rotate(box_wp, axis=(1, 0, 0), angle=90, center=(5, 5, 5))
    """
    if not isinstance(workplane, cq.Workplane):
        raise TypeError("workplane must be a CadQuery Workplane")

    # Validate axis is not zero vector
    if all(a == 0 for a in axis):
        raise ValueError("Axis cannot be the zero vector")

    return workplane.rotate(center, axis, angle)


def scale(
    workplane: cq.Workplane, x: float = 1, y: float = 1, z: float = 1
) -> cq.Workplane:
    """
    Scale a geometry by the specified factors.

    Args:
        workplane: The workplane/geometry to scale
        x: Scale factor in X direction (default: 1)
        y: Scale factor in Y direction (default: 1)
        z: Scale factor in Z direction (default: 1)

    Returns:
        A new Workplane with the scaled geometry

    Raises:
        ValueError: If any scale factor is <= 0

    Examples:
        >>> box_wp = box(10, 10, 10)
        >>> scaled_box = scale(box_wp, x=2, y=2, z=2)  # Double size
        >>> stretched_box = scale(box_wp, x=3, y=1, z=1)  # Stretch in X
    """
    if not isinstance(workplane, cq.Workplane):
        raise TypeError("workplane must be a CadQuery Workplane")

    if x <= 0 or y <= 0 or z <= 0:
        raise ValueError("All scale factors must be positive")

    # CadQuery doesn't have a direct scale method, so we need to use a transformation matrix
    # For uniform scaling, we can use the scale parameter in various operations
    # For now, we'll create a scaled version using a workaround

    # Get all solids from the workplane
    solids = workplane.solids().vals()

    if not solids:
        raise ValueError("Workplane contains no solids to scale")

    # For each solid, we need to scale it
    # CadQuery's transformGeometry with a scale matrix
    result = cq.Workplane("XY")

    for solid in solids:
        # Create a transformation matrix for scaling
        from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform
        from OCP.gp import gp_GTrsf

        # Create a general transformation with scale
        gtrsf = gp_GTrsf()
        gtrsf.SetValue(1, 1, x)
        gtrsf.SetValue(2, 2, y)
        gtrsf.SetValue(3, 3, z)

        # Apply the transformation to the shape
        transform = BRepBuilderAPI_GTransform(solid.wrapped, gtrsf, True)
        transform.Build()
        scaled_shape = transform.Shape()

        # Add to result
        result = result.add(cq.Shape.cast(scaled_shape))

    return result
