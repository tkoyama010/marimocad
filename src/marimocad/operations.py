"""
Advanced CAD operations for creating 3D geometries from 2D profiles.

This module provides functions for extruding, revolving, and sweeping
2D profiles to create 3D geometries.
"""

from typing import Tuple, Union

import cadquery as cq

from marimocad.sketch import Sketch


def extrude(
    profile: Union[cq.Workplane, Sketch],
    distance: float,
    both: bool = False,
    combine: bool = True,
) -> cq.Workplane:
    """
    Extrude a 2D profile to create a 3D geometry.

    Args:
        profile: The 2D profile to extrude (Workplane or Sketch)
        distance: Distance to extrude
        both: If True, extrude in both directions (default: False)
        combine: If True, combine with existing geometry (default: True)

    Returns:
        A Workplane containing the extruded geometry

    Raises:
        ValueError: If distance is 0
        TypeError: If profile is not a Workplane or Sketch

    Examples:
        >>> sketch = Sketch().circle(10)
        >>> cylinder_shape = extrude(sketch, 20)
        >>> double_sided = extrude(sketch, 10, both=True)
    """
    if distance == 0:
        raise ValueError("Extrude distance cannot be zero")

    # Get the workplane from the profile
    if isinstance(profile, Sketch):
        wp = profile.get_workplane()
    elif isinstance(profile, cq.Workplane):
        wp = profile
    else:
        raise TypeError("Profile must be a Workplane or Sketch")

    return wp.extrude(distance, both=both, combine=combine)


def revolve(
    profile: Union[cq.Workplane, Sketch],
    angle: float = 360,
    axis: Tuple[float, float, float] = (0, 0, 1),
    axis_start: Tuple[float, float, float] = (0, 0, 0),
    combine: bool = True,
) -> cq.Workplane:
    """
    Revolve a 2D profile around an axis to create a 3D geometry.

    Args:
        profile: The 2D profile to revolve (Workplane or Sketch)
        angle: Angle to revolve in degrees (default: 360 for full revolution)
        axis: Axis of revolution as (x, y, z) (default: Z-axis)
        axis_start: Start point of the axis as (x, y, z) (default: origin)
        combine: If True, combine with existing geometry (default: True)

    Returns:
        A Workplane containing the revolved geometry

    Raises:
        ValueError: If angle is 0 or axis is zero vector
        TypeError: If profile is not a Workplane or Sketch

    Examples:
        >>> sketch = Sketch().rectangle(10, 20, centered=False)
        >>> vase = revolve(sketch, angle=360)
        >>> half_vase = revolve(sketch, angle=180)
    """
    if angle == 0:
        raise ValueError("Revolve angle cannot be zero")

    if all(a == 0 for a in axis):
        raise ValueError("Axis cannot be the zero vector")

    # Get the workplane from the profile
    if isinstance(profile, Sketch):
        wp = profile.get_workplane()
    elif isinstance(profile, cq.Workplane):
        wp = profile
    else:
        raise TypeError("Profile must be a Workplane or Sketch")

    return wp.revolve(angle, axis_start, axis, combine=combine)


def sweep(
    profile: Union[cq.Workplane, Sketch],
    path: Union[cq.Workplane, cq.Wire],
    combine: bool = True,
    make_solid: bool = True,
) -> cq.Workplane:
    """
    Sweep a 2D profile along a path to create a 3D geometry.

    Args:
        profile: The 2D profile to sweep (Workplane or Sketch)
        path: The path to sweep along (Workplane with wire or Wire object)
        combine: If True, combine with existing geometry (default: True)
        make_solid: If True, create a solid (default: True)

    Returns:
        A Workplane containing the swept geometry

    Raises:
        TypeError: If profile or path are not of correct types
        ValueError: If path contains no wires

    Examples:
        >>> # Create a circular profile
        >>> profile = Sketch().circle(2)
        >>> # Create a path (helix-like path would be created differently)
        >>> path = cq.Workplane("XZ").lineTo(10, 0).lineTo(20, 10).lineTo(30, 10)
        >>> pipe = sweep(profile, path)
    """
    # Get the workplane from the profile
    if isinstance(profile, Sketch):
        profile_wp = profile.get_workplane()
    elif isinstance(profile, cq.Workplane):
        profile_wp = profile
    else:
        raise TypeError("Profile must be a Workplane or Sketch")

    # Get the wire from the path
    if isinstance(path, cq.Wire):
        path_wire = path
    elif isinstance(path, cq.Workplane):
        # Get the wire from the workplane
        wires = path.wires().vals()
        if not wires:
            raise ValueError("Path workplane contains no wires")
        path_wire = wires[0]
    else:
        raise TypeError("Path must be a Workplane or Wire")

    # Perform the sweep
    return profile_wp.sweep(path_wire, combine=combine, makeSolid=make_solid)
