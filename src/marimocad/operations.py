"""Boolean operations for combining shapes.

This module provides operations for combining multiple shapes using
constructive solid geometry (CSG) operations.

Examples:
    Combine shapes with union::

        from marimocad import Box, Cylinder, union
        box = Box(width=10, height=10, depth=10)
        cyl = Cylinder(radius=3, height=15)
        combined = union(box, cyl)

    Create a difference (subtraction)::

        from marimocad import Box, Sphere, difference
        box = Box(width=10, height=10, depth=10)
        sphere = Sphere(radius=6)
        result = difference(box, sphere)
"""

from typing import List
import numpy as np
from .shapes import Shape


class Operation(Shape):
    """Base class for boolean operations on shapes.
    
    Attributes:
        shapes: List of shapes involved in the operation.
    """
    
    def __init__(self, *shapes: Shape, name: str = "") -> None:
        """Initialize an operation.
        
        Args:
            *shapes: The shapes to combine.
            name: Optional name for the operation result.
        
        Raises:
            ValueError: If fewer than 2 shapes are provided.
        """
        super().__init__(name)
        if len(shapes) < 2:
            raise ValueError("Operations require at least 2 shapes")
        self.shapes = list(shapes)


class Union(Operation):
    """Union operation combining multiple shapes.
    
    The union creates a shape that includes all volume from all input shapes.
    
    Examples:
        Combine two boxes::
        
            box1 = Box(width=5, height=5, depth=5)
            box2 = Box(width=3, height=8, depth=3)
            result = Union(box1, box2)
    """
    
    def get_bounds(self) -> tuple:
        """Get the bounding box of the union.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        bounds = [shape.get_bounds() for shape in self.shapes]
        mins = np.min([b[0] for b in bounds], axis=0)
        maxs = np.max([b[1] for b in bounds], axis=0)
        return (mins, maxs)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"Union({len(self.shapes)} shapes)"


class Intersection(Operation):
    """Intersection operation of multiple shapes.
    
    The intersection creates a shape that only includes volume present
    in all input shapes.
    
    Examples:
        Find intersection of two shapes::
        
            box = Box(width=10, height=10, depth=10)
            sphere = Sphere(radius=6)
            result = Intersection(box, sphere)
    """
    
    def get_bounds(self) -> tuple:
        """Get the bounding box of the intersection.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        bounds = [shape.get_bounds() for shape in self.shapes]
        mins = np.max([b[0] for b in bounds], axis=0)
        maxs = np.min([b[1] for b in bounds], axis=0)
        return (mins, maxs)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"Intersection({len(self.shapes)} shapes)"


class Difference(Operation):
    """Difference operation (subtraction) of shapes.
    
    The difference removes the volume of the second shape from the first.
    
    Examples:
        Subtract a sphere from a box::
        
            box = Box(width=10, height=10, depth=10)
            sphere = Sphere(radius=6)
            result = Difference(box, sphere)
    """
    
    def __init__(self, base: Shape, *to_subtract: Shape, name: str = "") -> None:
        """Initialize a difference operation.
        
        Args:
            base: The base shape to subtract from.
            *to_subtract: Shapes to subtract from the base.
            name: Optional name for the result.
        
        Raises:
            ValueError: If no shapes to subtract are provided.
        """
        if not to_subtract:
            raise ValueError("Difference requires at least one shape to subtract")
        super().__init__(base, *to_subtract, name=name)
        self.base = base
        self.to_subtract = list(to_subtract)
    
    def get_bounds(self) -> tuple:
        """Get the bounding box of the difference.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        return self.base.get_bounds()
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"Difference(base, {len(self.to_subtract)} subtracted)"


def union(*shapes: Shape, name: str = "") -> Union:
    """Create a union of multiple shapes.
    
    Args:
        *shapes: The shapes to combine.
        name: Optional name for the result.
    
    Returns:
        A Union operation combining all shapes.
    
    Examples:
        Combine multiple shapes::
        
            box = Box(width=5, height=5, depth=5)
            sphere = Sphere(radius=3)
            cylinder = Cylinder(radius=2, height=10)
            result = union(box, sphere, cylinder)
    """
    return Union(*shapes, name=name)


def intersection(*shapes: Shape, name: str = "") -> Intersection:
    """Create an intersection of multiple shapes.
    
    Args:
        *shapes: The shapes to intersect.
        name: Optional name for the result.
    
    Returns:
        An Intersection operation of all shapes.
    
    Examples:
        Find common volume::
        
            box = Box(width=10, height=10, depth=10)
            sphere = Sphere(radius=6)
            result = intersection(box, sphere)
    """
    return Intersection(*shapes, name=name)


def difference(base: Shape, *to_subtract: Shape, name: str = "") -> Difference:
    """Create a difference (subtraction) operation.
    
    Args:
        base: The base shape to subtract from.
        *to_subtract: Shapes to subtract from the base.
        name: Optional name for the result.
    
    Returns:
        A Difference operation.
    
    Examples:
        Subtract multiple shapes::
        
            box = Box(width=10, height=10, depth=10)
            sphere1 = Sphere(radius=3)
            sphere2 = Sphere(radius=2)
            result = difference(box, sphere1, sphere2)
    """
    return Difference(base, *to_subtract, name=name)
