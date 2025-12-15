"""Extrusion and revolution operations for marimocad.

This module provides operations to create 3D solids from 2D faces
through extrusion, revolution, lofting, and sweeping.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from build123d import Axis, Vector, extrude as b3d_extrude
from build123d import loft as b3d_loft
from build123d import revolve as b3d_revolve
from build123d import sweep as b3d_sweep

if TYPE_CHECKING:
    from marimocad._types import Face, Solid, Wire


def extrude(
    face: Face,
    distance: float,
    direction: tuple[float, float, float] = (0, 0, 1),
    taper: float = 0,
) -> Solid:
    """Extrude a 2D face to create a solid.

    Args:
        face: Face to extrude
        distance: Extrusion distance
        direction: Extrusion direction vector
        taper: Taper angle in degrees

    Returns:
        Extruded solid

    Example:
        >>> import marimocad as mc
        >>> circle = mc.circle(5)
        >>> cylinder = mc.extrude(circle, 10)
    """
    dir_vec = Vector(*direction).normalized()
    amount = dir_vec * distance

    if taper != 0:
        return b3d_extrude(face, amount=amount, taper=taper)
    return b3d_extrude(face, amount=amount)


def revolve(
    face: Face,
    angle: float = 360,
    axis: str | tuple[float, float, float] = "Z",
) -> Solid:
    """Revolve a 2D face around an axis.

    Args:
        face: Face to revolve
        angle: Revolution angle in degrees
        axis: Revolution axis ("X", "Y", "Z" or custom vector)

    Returns:
        Revolved solid

    Example:
        >>> import marimocad as mc
        >>> profile = mc.rectangle(5, 10)
        >>> bottle = mc.revolve(profile, 360)
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
        axis_vector = Axis(Vector(*axis))

    return b3d_revolve(face, axis=axis_vector, revolution_arc=angle)


def loft(
    faces: list[Face],
    *,
    ruled: bool = False,
) -> Solid:
    """Create a solid by lofting through faces.

    Args:
        faces: Ordered list of faces to loft through
        ruled: Use ruled surface if True

    Returns:
        Lofted solid

    Example:
        >>> import marimocad as mc
        >>> circle1 = mc.circle(5)
        >>> circle2 = mc.translate(mc.circle(3), z=10)
        >>> lofted = mc.loft([circle1, circle2])
    """
    min_faces = 2
    if len(faces) < min_faces:
        msg = "At least two faces are required for lofting"
        raise ValueError(msg)

    return b3d_loft(faces, ruled=ruled)


def sweep(
    face: Face,
    path: Wire,
) -> Solid:
    """Sweep a face along a path.

    Args:
        face: Face to sweep
        path: Path wire to follow

    Returns:
        Swept solid

    Example:
        >>> import marimocad as mc
        >>> circle = mc.circle(2)
        >>> # Create a path (wire) - this is simplified
        >>> from build123d import Polyline, Vector
        >>> path = Polyline(
        ...     Vector(0, 0, 0),
        ...     Vector(10, 0, 0),
        ...     Vector(10, 10, 0),
        ...     Vector(10, 10, 10)
        ... )
        >>> swept = mc.sweep(circle, path)
    """
    return b3d_sweep(face, path)


__all__ = [
    "extrude",
    "loft",
    "revolve",
    "sweep",
]
