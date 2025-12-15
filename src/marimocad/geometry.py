"""Geometry creation functions for marimocad.

This module provides functions for creating primitive 3D and 2D geometries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from build123d import Align, Location, Vector
from build123d import Box as B3DBox
from build123d import Circle as B3DCircle
from build123d import Cone as B3DCone
from build123d import Cylinder as B3DCylinder
from build123d import Polygon as B3DPolygon
from build123d import Rectangle as B3DRectangle
from build123d import Sphere as B3DSphere
from build123d import Torus as B3DTorus


if TYPE_CHECKING:
    from marimocad._types import Face, Solid


def box(
    length: float,
    width: float,
    height: float,
    *,
    center: bool = False,
) -> Solid:
    """Create a rectangular box.

    Args:
        length: Box length in X direction
        width: Box width in Y direction
        height: Box height in Z direction
        center: Center the box at origin if True

    Returns:
        A solid box geometry

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 20, 5)
        >>> centered_box = mc.box(10, 10, 10, center=True)
    """
    if center:
        return B3DBox(length, width, height, align=Align.CENTER)
    return B3DBox(length, width, height)


def sphere(radius: float, *, center: bool = True) -> Solid:
    """Create a sphere.

    Args:
        radius: Sphere radius
        center: Center the sphere at origin if True

    Returns:
        A solid sphere geometry

    Example:
        >>> import marimocad as mc
        >>> sphere = mc.sphere(5.0)
    """
    if not center:
        # Move sphere up by radius to place bottom at origin
        s = B3DSphere(radius)
        return s.moved(Location(Vector(0, 0, radius)))
    return B3DSphere(radius)


def cylinder(
    radius: float,
    height: float,
    *,
    center: bool = False,
) -> Solid:
    """Create a cylinder.

    Args:
        radius: Cylinder radius
        height: Cylinder height along Z axis
        center: Center the cylinder at origin if True

    Returns:
        A solid cylinder geometry

    Example:
        >>> import marimocad as mc
        >>> cyl = mc.cylinder(3, 10)
    """
    if center:
        return B3DCylinder(radius, height, align=Align.CENTER)
    return B3DCylinder(radius, height)


def cone(
    radius: float,
    height: float,
    top_radius: float = 0.1,
    *,
    center: bool = False,
) -> Solid:
    """Create a cone or frustum.

    Args:
        radius: Bottom radius
        height: Cone height along Z axis
        top_radius: Top radius (small positive for cone, larger for frustum)
        center: Center the cone at origin if True

    Returns:
        A solid cone geometry

    Example:
        >>> import marimocad as mc
        >>> cone = mc.cone(5, 10, top_radius=0.1)
        >>> frustum = mc.cone(5, 10, top_radius=2)
    """
    if center:
        return B3DCone(radius, height, top_radius, align=Align.CENTER)
    return B3DCone(radius, height, top_radius)


def torus(
    major_radius: float,
    minor_radius: float,
) -> Solid:
    """Create a torus.

    Args:
        major_radius: Distance from torus center to tube center
        minor_radius: Radius of the tube

    Returns:
        A solid torus geometry

    Example:
        >>> import marimocad as mc
        >>> torus = mc.torus(10, 2)
    """
    return B3DTorus(major_radius, minor_radius)


def circle(radius: float) -> Face:
    """Create a circular face.

    Args:
        radius: Circle radius

    Returns:
        A circular face

    Example:
        >>> import marimocad as mc
        >>> circle = mc.circle(5)
    """
    return B3DCircle(radius)


def rectangle(width: float, height: float) -> Face:
    """Create a rectangular face.

    Args:
        width: Rectangle width
        height: Rectangle height

    Returns:
        A rectangular face

    Example:
        >>> import marimocad as mc
        >>> rect = mc.rectangle(10, 20)
    """
    return B3DRectangle(width, height)


def polygon(points: list[tuple[float, float]]) -> Face:
    """Create a polygon from points.

    Args:
        points: List of (x, y) coordinate tuples

    Returns:
        A polygonal face

    Example:
        >>> import marimocad as mc
        >>> triangle = mc.polygon([(0, 0), (10, 0), (5, 10)])
    """
    vertices = [Vector(x, y, 0) for x, y in points]
    return B3DPolygon(*vertices)


__all__ = [
    "box",
    "circle",
    "cone",
    "cylinder",
    "polygon",
    "rectangle",
    "sphere",
    "torus",
]
