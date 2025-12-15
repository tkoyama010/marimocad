"""
Primitive shape creation functions.

This module provides functions to create basic 3D geometric primitives
such as boxes, spheres, cylinders, cones, and tori.
"""

from typing import Tuple
import cadquery as cq


def box(
    length: float, width: float, height: float, centered: bool = True
) -> cq.Workplane:
    """
    Create a rectangular box.

    Args:
        length: Length of the box (X dimension)
        width: Width of the box (Y dimension)
        height: Height of the box (Z dimension)
        centered: If True, center the box at origin. If False, place corner at origin.

    Returns:
        A CadQuery Workplane containing the box

    Raises:
        ValueError: If any dimension is <= 0

    Examples:
        >>> my_box = box(10, 20, 30)
        >>> small_box = box(1, 1, 1, centered=False)
    """
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("All dimensions must be positive")

    wp = cq.Workplane("XY")
    return wp.box(length, width, height, centered=centered)


def sphere(radius: float, angle1: float = -90, angle2: float = 90) -> cq.Workplane:
    """
    Create a sphere.

    Args:
        radius: Radius of the sphere
        angle1: Start angle for the sphere arc (default: -90)
        angle2: End angle for the sphere arc (default: 90)

    Returns:
        A CadQuery Workplane containing the sphere

    Raises:
        ValueError: If radius <= 0

    Examples:
        >>> my_sphere = sphere(10)
        >>> hemisphere = sphere(5, angle1=0, angle2=90)
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")

    wp = cq.Workplane("XY")
    return wp.sphere(radius, angle1=angle1, angle2=angle2)


def cylinder(
    radius: float, height: float, centered: bool = True, angle: float = 360
) -> cq.Workplane:
    """
    Create a cylinder.

    Args:
        radius: Radius of the cylinder
        height: Height of the cylinder
        centered: If True, center along Z axis. If False, base at origin.
        angle: Sweep angle in degrees (default: 360 for full cylinder)

    Returns:
        A CadQuery Workplane containing the cylinder

    Raises:
        ValueError: If radius <= 0 or height <= 0

    Examples:
        >>> my_cylinder = cylinder(5, 10)
        >>> half_cylinder = cylinder(3, 8, angle=180)
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")

    wp = cq.Workplane("XY")
    result = wp.cylinder(height, radius, angle=angle, centered=centered)
    return result


def cone(
    radius1: float,
    radius2: float,
    height: float,
    centered: bool = True,
    angle: float = 360,
) -> cq.Workplane:
    """
    Create a cone or frustum.

    Args:
        radius1: Radius at the base
        radius2: Radius at the top
        height: Height of the cone
        centered: If True, center along Z axis. If False, base at origin.
        angle: Sweep angle in degrees (default: 360)

    Returns:
        A CadQuery Workplane containing the cone

    Raises:
        ValueError: If any radius or height is negative

    Examples:
        >>> my_cone = cone(10, 0, 20)  # Pointed cone
        >>> frustum = cone(10, 5, 15)  # Truncated cone
    """
    if radius1 < 0 or radius2 < 0:
        raise ValueError("Radii must be non-negative")
    if height <= 0:
        raise ValueError("Height must be positive")
    if radius1 == 0 and radius2 == 0:
        raise ValueError("At least one radius must be positive")

    # Create cone using loft between two circles
    wp = cq.Workplane("XY")

    # Handle centering
    if centered:
        z1 = -height / 2
        z2 = height / 2
    else:
        z1 = 0
        z2 = height

    # Create bottom circle
    if radius1 > 0:
        wp = wp.workplane(offset=z1).circle(radius1)
    else:
        wp = wp.workplane(offset=z1).center(0, 0)

    # Create top circle
    if radius2 > 0:
        wp = wp.workplane(offset=height).circle(radius2)
    else:
        wp = wp.workplane(offset=height).center(0, 0)

    # Loft between them
    result = wp.loft()

    # Apply angle if not full
    if angle < 360:
        cutting_box = cq.Workplane("XZ").transformed(rotate=(0, 0, angle / 2))
        cutting_box = cutting_box.rect(radius1 * 3, height * 2).revolve(
            180 - angle, (0, 0, 0), (0, 0, 1)
        )
        result = result.cut(cutting_box)

    return result


def torus(
    major_radius: float, minor_radius: float, angle1: float = 0, angle2: float = 360
) -> cq.Workplane:
    """
    Create a torus (donut shape).

    Args:
        major_radius: Distance from center of torus to center of tube
        minor_radius: Radius of the tube
        angle1: Start angle for the sweep (default: 0)
        angle2: End angle for the sweep (default: 360)

    Returns:
        A CadQuery Workplane containing the torus

    Raises:
        ValueError: If any radius <= 0

    Examples:
        >>> my_torus = torus(20, 5)
        >>> half_torus = torus(15, 3, angle1=0, angle2=180)
    """
    if major_radius <= 0:
        raise ValueError("Major radius must be positive")
    if minor_radius <= 0:
        raise ValueError("Minor radius must be positive")

    wp = cq.Workplane("XY")
    wp = wp.transformed(offset=(major_radius, 0, 0))
    wp = wp.circle(minor_radius)

    # Calculate sweep angle
    sweep_angle = angle2 - angle1

    result = wp.revolve(sweep_angle, (0, 0, 0), (0, 0, 1))

    # If we need to rotate to start at angle1
    if angle1 != 0:
        result = result.rotate((0, 0, 0), (0, 0, 1), angle1)

    return result
