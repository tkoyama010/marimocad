"""
2D sketching operations for creating profiles.

This module provides a Sketch class for creating 2D profiles that can
be used with extrude, revolve, and sweep operations.
"""

from typing import Tuple

import cadquery as cq


class Sketch:
    """
    A 2D sketch for creating profiles.

    This class provides methods to create 2D shapes on a plane that can
    later be extruded, revolved, or swept to create 3D geometry.
    """

    def __init__(self, plane: str = "XY"):
        """
        Initialize a new Sketch.

        Args:
            plane: The plane to sketch on ("XY", "XZ", or "YZ")

        Raises:
            ValueError: If plane is not one of the valid options
        """
        valid_planes = ["XY", "XZ", "YZ"]
        if plane not in valid_planes:
            raise ValueError(f"Plane must be one of {valid_planes}")

        self._workplane = cq.Workplane(plane)
        self._plane = plane

    def rectangle(
        self, width: float, height: float, centered: bool = True
    ) -> "Sketch":
        """
        Add a rectangle to the sketch.

        Args:
            width: Width of the rectangle
            height: Height of the rectangle
            centered: If True, center at origin. If False, corner at origin.

        Returns:
            Self for method chaining

        Raises:
            ValueError: If width or height <= 0
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")

        self._workplane = self._workplane.rect(width, height, centered=centered)
        return self

    def circle(self, radius: float) -> "Sketch":
        """
        Add a circle to the sketch.

        Args:
            radius: Radius of the circle

        Returns:
            Self for method chaining

        Raises:
            ValueError: If radius <= 0
        """
        if radius <= 0:
            raise ValueError("Radius must be positive")

        self._workplane = self._workplane.circle(radius)
        return self

    def polygon(self, num_sides: int, diameter: float) -> "Sketch":
        """
        Add a regular polygon to the sketch.

        Args:
            num_sides: Number of sides for the polygon
            diameter: Diameter of the circumscribed circle

        Returns:
            Self for method chaining

        Raises:
            ValueError: If num_sides < 3 or diameter <= 0
        """
        if num_sides < 3:
            raise ValueError("Polygon must have at least 3 sides")
        if diameter <= 0:
            raise ValueError("Diameter must be positive")

        self._workplane = self._workplane.polygon(num_sides, diameter)
        return self

    def line(self, x: float, y: float) -> "Sketch":
        """
        Draw a line from the current point.

        Args:
            x: X offset from current point
            y: Y offset from current point

        Returns:
            Self for method chaining
        """
        self._workplane = self._workplane.line(x, y)
        return self

    def line_to(self, x: float, y: float) -> "Sketch":
        """
        Draw a line to an absolute point.

        Args:
            x: X coordinate of end point
            y: Y coordinate of end point

        Returns:
            Self for method chaining
        """
        self._workplane = self._workplane.lineTo(x, y)
        return self

    def arc(self, end_point: Tuple[float, float], radius: float) -> "Sketch":
        """
        Draw an arc from the current point.

        Args:
            end_point: End point of the arc as (x, y)
            radius: Radius of the arc (positive for convex, negative for concave)

        Returns:
            Self for method chaining

        Raises:
            ValueError: If radius is 0

        Note:
            The direction of the arc is determined by the sign of the radius.
            Positive radius creates a convex arc, negative creates a concave arc.
        """
        if radius == 0:
            raise ValueError("Radius cannot be zero")

        self._workplane = self._workplane.radiusArc(end_point, radius)
        return self

    def close(self) -> "Sketch":
        """
        Close the current sketch path.

        Returns:
            Self for method chaining
        """
        self._workplane = self._workplane.close()
        return self

    def move_to(self, x: float, y: float) -> "Sketch":
        """
        Move to a new point without drawing.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Self for method chaining
        """
        self._workplane = self._workplane.moveTo(x, y)
        return self

    def get_workplane(self) -> cq.Workplane:
        """
        Get the underlying CadQuery Workplane.

        Returns:
            The CadQuery Workplane containing the sketch
        """
        return self._workplane

    def __repr__(self) -> str:
        """String representation of the Sketch."""
        return f"Sketch(plane='{self._plane}')"
