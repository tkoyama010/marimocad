"""Basic 3D shapes for CAD modeling.

This module provides fundamental 3D geometric shapes that can be used
as building blocks for more complex CAD models.

Examples:
    Create a simple box::

        from marimocad import Box
        box = Box(width=10, height=5, depth=3)

    Create a cylinder::

        from marimocad import Cylinder
        cylinder = Cylinder(radius=5, height=10)

    Create a sphere::

        from marimocad import Sphere
        sphere = Sphere(radius=5)
"""

from typing import Tuple
import numpy as np


class Shape:
    """Base class for all 3D shapes.
    
    Attributes:
        position: The (x, y, z) position of the shape's center.
        name: Optional name for the shape.
    """
    
    def __init__(self, name: str = "") -> None:
        """Initialize a shape.
        
        Args:
            name: Optional name for the shape.
        """
        self.position = np.array([0.0, 0.0, 0.0])
        self.name = name
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the shape.
        
        Returns:
            A tuple of (min_point, max_point) representing the axis-aligned
            bounding box.
        """
        raise NotImplementedError("Subclasses must implement get_bounds()")
    
    def __repr__(self) -> str:
        """Return string representation of the shape."""
        if self.name:
            return f"{self.__class__.__name__}(name='{self.name}')"
        return f"{self.__class__.__name__}()"


class Box(Shape):
    """A rectangular box (cuboid) shape.
    
    Attributes:
        width: The width (x-dimension) of the box.
        height: The height (y-dimension) of the box.
        depth: The depth (z-dimension) of the box.
    
    Examples:
        Create a box with specific dimensions::
        
            box = Box(width=10, height=5, depth=3)
            print(f"Box volume: {box.volume()}")
        
        Create a cube::
        
            cube = Box(width=5, height=5, depth=5, name="my_cube")
    """
    
    def __init__(
        self,
        width: float = 1.0,
        height: float = 1.0,
        depth: float = 1.0,
        name: str = "",
    ) -> None:
        """Initialize a box shape.
        
        Args:
            width: The width (x-dimension) of the box. Must be positive.
            height: The height (y-dimension) of the box. Must be positive.
            depth: The depth (z-dimension) of the box. Must be positive.
            name: Optional name for the box.
        
        Raises:
            ValueError: If any dimension is not positive.
        """
        super().__init__(name)
        if width <= 0 or height <= 0 or depth <= 0:
            raise ValueError("All dimensions must be positive")
        self.width = width
        self.height = height
        self.depth = depth
    
    def volume(self) -> float:
        """Calculate the volume of the box.
        
        Returns:
            The volume in cubic units.
        """
        return self.width * self.height * self.depth
    
    def surface_area(self) -> float:
        """Calculate the surface area of the box.
        
        Returns:
            The surface area in square units.
        """
        return 2 * (
            self.width * self.height
            + self.height * self.depth
            + self.depth * self.width
        )
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the box.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        half_dims = np.array([self.width, self.height, self.depth]) / 2
        return (self.position - half_dims, self.position + half_dims)
    
    def __repr__(self) -> str:
        """Return string representation of the box."""
        return (
            f"Box(width={self.width}, height={self.height}, "
            f"depth={self.depth}, name='{self.name}')"
        )


class Cylinder(Shape):
    """A cylindrical shape.
    
    Attributes:
        radius: The radius of the cylinder.
        height: The height of the cylinder.
    
    Examples:
        Create a cylinder::
        
            cylinder = Cylinder(radius=5, height=10)
            print(f"Cylinder volume: {cylinder.volume()}")
    """
    
    def __init__(
        self,
        radius: float = 1.0,
        height: float = 1.0,
        name: str = "",
    ) -> None:
        """Initialize a cylinder shape.
        
        Args:
            radius: The radius of the cylinder. Must be positive.
            height: The height of the cylinder. Must be positive.
            name: Optional name for the cylinder.
        
        Raises:
            ValueError: If radius or height is not positive.
        """
        super().__init__(name)
        if radius <= 0 or height <= 0:
            raise ValueError("Radius and height must be positive")
        self.radius = radius
        self.height = height
    
    def volume(self) -> float:
        """Calculate the volume of the cylinder.
        
        Returns:
            The volume in cubic units.
        """
        return np.pi * self.radius**2 * self.height
    
    def surface_area(self) -> float:
        """Calculate the surface area of the cylinder.
        
        Returns:
            The surface area in square units.
        """
        return 2 * np.pi * self.radius * (self.radius + self.height)
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the cylinder.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        half_height = self.height / 2
        return (
            self.position + np.array([-self.radius, -self.radius, -half_height]),
            self.position + np.array([self.radius, self.radius, half_height]),
        )
    
    def __repr__(self) -> str:
        """Return string representation of the cylinder."""
        return (
            f"Cylinder(radius={self.radius}, height={self.height}, "
            f"name='{self.name}')"
        )


class Sphere(Shape):
    """A spherical shape.
    
    Attributes:
        radius: The radius of the sphere.
    
    Examples:
        Create a sphere::
        
            sphere = Sphere(radius=5)
            print(f"Sphere volume: {sphere.volume()}")
    """
    
    def __init__(self, radius: float = 1.0, name: str = "") -> None:
        """Initialize a sphere shape.
        
        Args:
            radius: The radius of the sphere. Must be positive.
            name: Optional name for the sphere.
        
        Raises:
            ValueError: If radius is not positive.
        """
        super().__init__(name)
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius
    
    def volume(self) -> float:
        """Calculate the volume of the sphere.
        
        Returns:
            The volume in cubic units.
        """
        return (4 / 3) * np.pi * self.radius**3
    
    def surface_area(self) -> float:
        """Calculate the surface area of the sphere.
        
        Returns:
            The surface area in square units.
        """
        return 4 * np.pi * self.radius**2
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the sphere.
        
        Returns:
            A tuple of (min_point, max_point).
        """
        offset = np.array([self.radius, self.radius, self.radius])
        return (self.position - offset, self.position + offset)
    
    def __repr__(self) -> str:
        """Return string representation of the sphere."""
        return f"Sphere(radius={self.radius}, name='{self.name}')"
