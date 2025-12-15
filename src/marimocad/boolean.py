"""
Boolean operations for combining CAD geometries.

This module provides functions to perform boolean operations such as
union, difference, and intersection on geometries.
"""

import cadquery as cq


def union(*workplanes: cq.Workplane) -> cq.Workplane:
    """
    Perform a union (combine) operation on multiple geometries.

    Args:
        *workplanes: Variable number of Workplanes to union together

    Returns:
        A new Workplane containing the union of all input geometries

    Raises:
        ValueError: If fewer than 2 workplanes are provided
        TypeError: If any input is not a Workplane

    Examples:
        >>> box1 = box(10, 10, 10)
        >>> box2 = translate(box(5, 5, 5), x=7)
        >>> combined = union(box1, box2)
    """
    if len(workplanes) < 2:
        raise ValueError("Union requires at least 2 workplanes")

    for wp in workplanes:
        if not isinstance(wp, cq.Workplane):
            raise TypeError("All arguments must be CadQuery Workplanes")

    # Start with the first workplane
    result = workplanes[0]

    # Union with each subsequent workplane
    for wp in workplanes[1:]:
        result = result.union(wp)

    return result


def difference(base: cq.Workplane, *tools: cq.Workplane) -> cq.Workplane:
    """
    Subtract one or more geometries from a base geometry.

    Args:
        base: The base workplane to subtract from
        *tools: Variable number of tool Workplanes to subtract

    Returns:
        A new Workplane with the tools subtracted from the base

    Raises:
        ValueError: If no tool workplanes are provided
        TypeError: If any input is not a Workplane

    Examples:
        >>> box_wp = box(20, 20, 20)
        >>> hole = cylinder(5, 25)
        >>> box_with_hole = difference(box_wp, hole)
    """
    if not isinstance(base, cq.Workplane):
        raise TypeError("Base must be a CadQuery Workplane")

    if len(tools) == 0:
        raise ValueError("Difference requires at least one tool workplane")

    for tool in tools:
        if not isinstance(tool, cq.Workplane):
            raise TypeError("All tools must be CadQuery Workplanes")

    # Start with the base
    result = base

    # Cut each tool from the result
    for tool in tools:
        result = result.cut(tool)

    return result


def intersection(*workplanes: cq.Workplane) -> cq.Workplane:
    """
    Perform an intersection operation on multiple geometries.

    Returns only the volume that is common to all input geometries.

    Args:
        *workplanes: Variable number of Workplanes to intersect

    Returns:
        A new Workplane containing the intersection of all input geometries

    Raises:
        ValueError: If fewer than 2 workplanes are provided
        TypeError: If any input is not a Workplane

    Examples:
        >>> box1 = box(20, 20, 20)
        >>> box2 = translate(box(20, 20, 20), x=10)
        >>> overlap = intersection(box1, box2)
    """
    if len(workplanes) < 2:
        raise ValueError("Intersection requires at least 2 workplanes")

    for wp in workplanes:
        if not isinstance(wp, cq.Workplane):
            raise TypeError("All arguments must be CadQuery Workplanes")

    # Start with the first workplane
    result = workplanes[0]

    # Intersect with each subsequent workplane
    for wp in workplanes[1:]:
        result = result.intersect(wp)

    return result
