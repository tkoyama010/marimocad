"""Operations for transforming and combining geometries.

This module provides transformation operations (translate, rotate, scale, mirror)
and boolean operations (union, subtract, intersect) for CAD geometries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from build123d import Axis, Location, Plane, Rotation, Vector


if TYPE_CHECKING:
    from marimocad._types import Geometry


def translate(
    geom: Geometry,
    x: float = 0,
    y: float = 0,
    z: float = 0,
) -> Geometry:
    """Translate geometry by offset.

    Args:
        geom: Geometry to translate
        x: X offset
        y: Y offset
        z: Z offset

    Returns:
        Translated geometry

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> moved = mc.translate(box, x=5, y=10)
    """
    return geom.moved(Location(Vector(x, y, z)))


def rotate(
    geom: Geometry,
    angle: float,
    axis: str | tuple[float, float, float] = "Z",
    center: tuple[float, float, float] | None = None,
) -> Geometry:
    """Rotate geometry around an axis.

    Args:
        geom: Geometry to rotate
        angle: Rotation angle in degrees
        axis: Rotation axis ("X", "Y", "Z" or custom vector)
        center: Center of rotation (origin if None)

    Returns:
        Rotated geometry

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> rotated = mc.rotate(box, 45, axis="Z")
    """
    # Parse axis
    if isinstance(axis, str):
        axis_upper = axis.upper()
        if axis_upper == "X":
            axis_vector = Axis.X
        elif axis_upper == "Y":
            axis_vector = Axis.Y
        elif axis_upper == "Z":
            axis_vector = Axis.Z
        else:
            msg = f"Invalid axis string: {axis}. Use 'X', 'Y', or 'Z'"
            raise ValueError(msg)
    else:
        axis_vector = Vector(*axis)

    # Create rotation
    rotation = Rotation(axis_vector, angle)

    # If center is specified, need to translate, rotate, translate back
    if center is not None:
        center_vec = Vector(*center)
        # Move to origin
        geom = geom.moved(Location(-center_vec))
        # Rotate
        geom = geom.moved(rotation)
        # Move back
        return geom.moved(Location(center_vec))

    return geom.moved(rotation)


def scale(
    geom: Geometry,
    factor: float,
    center: tuple[float, float, float] | None = None,
) -> Geometry:
    """Scale geometry uniformly.

    Args:
        geom: Geometry to scale
        factor: Uniform scale factor
        center: Center of scaling (origin if None)

    Returns:
        Scaled geometry

    Note:
        Currently only uniform scaling is supported due to backend limitations.
        Non-uniform scaling may be added in a future version.

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> bigger = mc.scale(box, 2.0)
    """
    center_vec = Vector(0, 0, 0) if center is None else Vector(*center)

    # Move to origin, scale, move back
    if center is not None:
        # Translate to origin
        translated = geom.moved(Location(Vector(-center_vec.X, -center_vec.Y, -center_vec.Z)))
        # Scale
        scaled = translated.scale(factor)
        # Translate back
        return scaled.moved(Location(center_vec))

    return geom.scale(factor)


def mirror(
    geom: Geometry,
    plane: str | tuple[float, float, float] = "XY",
) -> Geometry:
    """Mirror geometry across a plane.

    Args:
        geom: Geometry to mirror
        plane: Mirror plane ("XY", "YZ", "XZ" or normal vector)

    Returns:
        Mirrored geometry

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> mirrored = mc.mirror(box, plane="XY")
    """
    # Parse plane
    if isinstance(plane, str):
        plane_upper = plane.upper()
        if plane_upper == "XY":
            mirror_plane = Plane.XY
        elif plane_upper == "YZ":
            mirror_plane = Plane.YZ
        elif plane_upper == "XZ":
            mirror_plane = Plane.XZ
        else:
            msg = f"Invalid plane string: {plane}. Use 'XY', 'YZ', or 'XZ'"
            raise ValueError(msg)
    else:
        # Custom plane with normal vector
        normal = Vector(*plane)
        mirror_plane = Plane(origin=Vector(0, 0, 0), x_dir=normal)

    return geom.mirror(mirror_plane)


def union(*geoms: Geometry) -> Geometry:
    """Combine geometries (logical OR).

    Args:
        *geoms: Geometries to union

    Returns:
        Combined geometry

    Example:
        >>> import marimocad as mc
        >>> box1 = mc.box(10, 10, 10)
        >>> box2 = mc.translate(mc.box(10, 10, 10), x=5)
        >>> combined = mc.union(box1, box2)
    """
    if not geoms:
        msg = "At least one geometry is required for union"
        raise ValueError(msg)

    if len(geoms) == 1:
        return geoms[0]

    result = geoms[0]
    for geom in geoms[1:]:
        result = result + geom
    return result


def subtract(base: Geometry, *tools: Geometry) -> Geometry:
    """Subtract tool geometries from base (logical difference).

    Args:
        base: Base geometry
        *tools: Geometries to subtract

    Returns:
        Result geometry with tools removed

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(20, 20, 10)
        >>> cyl = mc.cylinder(3, 15)
        >>> result = mc.subtract(box, cyl)
    """
    if not tools:
        return base

    result = base
    for tool in tools:
        result = result - tool
    return result


def intersect(*geoms: Geometry) -> Geometry:
    """Intersect geometries (logical AND).

    Args:
        *geoms: Geometries to intersect

    Returns:
        Intersection geometry

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> sphere = mc.sphere(6)
        >>> result = mc.intersect(box, sphere)
    """
    if not geoms:
        msg = "At least one geometry is required for intersection"
        raise ValueError(msg)

    if len(geoms) == 1:
        return geoms[0]

    result = geoms[0]
    for geom in geoms[1:]:
        result = result & geom
    return result


__all__ = [
    "intersect",
    "mirror",
    "rotate",
    "scale",
    "subtract",
    "translate",
    "union",
]
