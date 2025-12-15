# marimocad Data Structures

This document defines the core data structures and type system used in marimocad for representing CAD geometry and related entities.

## Type System Overview

marimocad uses a Protocol-based type system that provides:
- **Type safety**: Static type checking with mypy
- **Flexibility**: Works with multiple backends
- **Duck typing**: Any object implementing the protocol is valid
- **No wrapping**: Backend objects used directly where possible

## Core Geometry Types

### Base Geometry Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Geometry(Protocol):
    """Base protocol for all geometric entities.
    
    Any object implementing these methods can be used as geometry
    in marimocad operations.
    """
    
    def bounding_box(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the axis-aligned bounding box.
        
        Returns:
            ((xmin, ymin, zmin), (xmax, ymax, zmax))
        """
        ...
    
    def center(self) -> tuple[float, float, float]:
        """Get the geometric center point.
        
        Returns:
            (x, y, z) coordinates of center
        """
        ...
    
    def translate(self, x: float = 0, y: float = 0, z: float = 0) -> "Geometry":
        """Translate the geometry.
        
        Args:
            x: Translation in X direction
            y: Translation in Y direction
            z: Translation in Z direction
            
        Returns:
            New translated geometry
        """
        ...
    
    def rotate(
        self,
        angle: float,
        axis: tuple[float, float, float] = (0, 0, 1),
        center: tuple[float, float, float] | None = None,
    ) -> "Geometry":
        """Rotate the geometry.
        
        Args:
            angle: Rotation angle in degrees
            axis: Rotation axis as (x, y, z) vector
            center: Center of rotation (origin if None)
            
        Returns:
            New rotated geometry
        """
        ...
```

### Solid (3D Geometry)

```python
@runtime_checkable
class Solid(Geometry, Protocol):
    """3D solid geometry with volume.
    
    Represents closed, manifold 3D shapes like boxes, spheres, etc.
    """
    
    def volume(self) -> float:
        """Calculate the volume of the solid.
        
        Returns:
            Volume in cubic units
        """
        ...
    
    def surface_area(self) -> float:
        """Calculate the total surface area.
        
        Returns:
            Surface area in square units
        """
        ...
    
    def faces(self) -> list["Face"]:
        """Get all faces of the solid.
        
        Returns:
            List of Face objects forming the boundary
        """
        ...
    
    def edges(self) -> list["Edge"]:
        """Get all edges of the solid.
        
        Returns:
            List of Edge objects
        """
        ...
    
    def vertices(self) -> list["Vertex"]:
        """Get all vertices of the solid.
        
        Returns:
            List of Vertex objects
        """
        ...
    
    def is_valid(self) -> bool:
        """Check if the solid is geometrically valid.
        
        Returns:
            True if valid manifold solid
        """
        ...
```

### Face (2D Surface)

```python
@runtime_checkable
class Face(Geometry, Protocol):
    """2D surface geometry.
    
    Represents a surface with optional holes, can be planar or curved.
    """
    
    def area(self) -> float:
        """Calculate the surface area.
        
        Returns:
            Area in square units
        """
        ...
    
    def normal(self, u: float = 0.5, v: float = 0.5) -> tuple[float, float, float]:
        """Get the surface normal at parametric coordinates.
        
        Args:
            u: Parameter in U direction (0 to 1)
            v: Parameter in V direction (0 to 1)
            
        Returns:
            (x, y, z) unit normal vector
        """
        ...
    
    def edges(self) -> list["Edge"]:
        """Get boundary edges of the face.
        
        Returns:
            List of Edge objects forming the boundary
        """
        ...
    
    def wires(self) -> list["Wire"]:
        """Get boundary wires.
        
        Returns:
            List of Wire objects (outer boundary + holes)
        """
        ...
    
    def is_planar(self) -> bool:
        """Check if the face is planar.
        
        Returns:
            True if face lies in a plane
        """
        ...
```

### Edge (1D Curve)

```python
@runtime_checkable
class Edge(Geometry, Protocol):
    """1D curve geometry.
    
    Represents a curve segment between two vertices.
    """
    
    def length(self) -> float:
        """Calculate the length of the edge.
        
        Returns:
            Length in linear units
        """
        ...
    
    def vertices(self) -> list["Vertex"]:
        """Get the end vertices.
        
        Returns:
            List of exactly 2 Vertex objects (start and end)
        """
        ...
    
    def tangent(self, t: float = 0.5) -> tuple[float, float, float]:
        """Get the tangent vector at parameter t.
        
        Args:
            t: Parameter along edge (0 to 1)
            
        Returns:
            (x, y, z) unit tangent vector
        """
        ...
    
    def point_at(self, t: float) -> tuple[float, float, float]:
        """Get point at parameter t.
        
        Args:
            t: Parameter along edge (0 to 1)
            
        Returns:
            (x, y, z) coordinates
        """
        ...
    
    def is_linear(self) -> bool:
        """Check if edge is a straight line.
        
        Returns:
            True if edge is linear
        """
        ...
```

### Vertex (0D Point)

```python
@runtime_checkable
class Vertex(Geometry, Protocol):
    """0D point geometry.
    
    Represents a point in 3D space.
    """
    
    def position(self) -> tuple[float, float, float]:
        """Get the vertex position.
        
        Returns:
            (x, y, z) coordinates
        """
        ...
    
    def x(self) -> float:
        """Get X coordinate."""
        ...
    
    def y(self) -> float:
        """Get Y coordinate."""
        ...
    
    def z(self) -> float:
        """Get Z coordinate."""
        ...
```

### Wire (Connected Edges)

```python
@runtime_checkable
class Wire(Geometry, Protocol):
    """Sequence of connected edges forming a path.
    
    Can be open or closed. Used for profiles, paths, and boundaries.
    """
    
    def edges(self) -> list[Edge]:
        """Get all edges in order.
        
        Returns:
            List of Edge objects in connected sequence
        """
        ...
    
    def vertices(self) -> list[Vertex]:
        """Get all vertices in order.
        
        Returns:
            List of Vertex objects
        """
        ...
    
    def is_closed(self) -> bool:
        """Check if wire forms a closed loop.
        
        Returns:
            True if first and last vertices coincide
        """
        ...
    
    def length(self) -> float:
        """Calculate total length.
        
        Returns:
            Sum of all edge lengths
        """
        ...
```

## Assembly Data Structures

### Part

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class Part:
    """A part in an assembly with position and metadata.
    
    Attributes:
        name: Unique identifier for the part
        geometry: The geometric representation
        position: Translation (x, y, z)
        rotation: Rotation angles (rx, ry, rz) in degrees
        metadata: Additional custom data
    """
    
    name: str
    geometry: Geometry
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    metadata: dict[str, Any] = None
    
    def __post_init__(self) -> None:
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}
    
    def transform(self) -> Geometry:
        """Get the transformed geometry.
        
        Returns:
            Geometry with position and rotation applied
        """
        import marimocad as mc
        
        # Apply rotation first
        geom = self.geometry
        if any(self.rotation):
            if self.rotation[0]:
                geom = mc.rotate(geom, self.rotation[0], axis="X")
            if self.rotation[1]:
                geom = mc.rotate(geom, self.rotation[1], axis="Y")
            if self.rotation[2]:
                geom = mc.rotate(geom, self.rotation[2], axis="Z")
        
        # Then translation
        if any(self.position):
            geom = mc.translate(geom, *self.position)
        
        return geom
```

### Constraint

```python
from enum import Enum

class ConstraintType(Enum):
    """Types of assembly constraints."""
    
    MATE = "mate"                # Face-to-face contact
    ALIGN = "align"              # Align axes or planes
    DISTANCE = "distance"        # Fixed distance between entities
    ANGLE = "angle"              # Fixed angle between entities
    PARALLEL = "parallel"        # Keep entities parallel
    PERPENDICULAR = "perpendicular"  # Keep entities perpendicular
    CONCENTRIC = "concentric"    # Share same axis
    TANGENT = "tangent"          # Tangent contact

@dataclass
class Constraint:
    """A constraint between assembly parts.
    
    Attributes:
        type: Type of constraint
        part1: Name of first part
        part2: Name of second part
        entities1: Entities from part1 (faces, edges, etc.)
        entities2: Entities from part2
        parameters: Additional constraint parameters
    """
    
    type: ConstraintType
    part1: str
    part2: str
    entities1: list[Geometry] | None = None
    entities2: list[Geometry] | None = None
    parameters: dict[str, Any] = None
    
    def __post_init__(self) -> None:
        """Initialize parameters if not provided."""
        if self.parameters is None:
            self.parameters = {}
```

### Assembly

```python
class Assembly:
    """Container for multi-part assemblies with constraints.
    
    Manages multiple parts with relative positioning and constraints
    between them.
    
    Attributes:
        name: Assembly name
        parts: Dictionary of parts by name
        constraints: List of constraints
    """
    
    def __init__(self, name: str = "assembly") -> None:
        """Initialize assembly.
        
        Args:
            name: Assembly name
        """
        self.name = name
        self._parts: dict[str, Part] = {}
        self._constraints: list[Constraint] = []
    
    def add_part(
        self,
        geometry: Geometry,
        name: str,
        position: tuple[float, float, float] = (0, 0, 0),
        rotation: tuple[float, float, float] = (0, 0, 0),
        **metadata: Any,
    ) -> None:
        """Add a part to the assembly.
        
        Args:
            geometry: Part geometry
            name: Unique part name
            position: Part position (x, y, z)
            rotation: Part rotation (rx, ry, rz) in degrees
            **metadata: Additional part metadata
            
        Raises:
            ValueError: If part name already exists
        """
        if name in self._parts:
            raise ValueError(f"Part '{name}' already exists")
        
        self._parts[name] = Part(
            name=name,
            geometry=geometry,
            position=position,
            rotation=rotation,
            metadata=metadata,
        )
    
    def get_part(self, name: str) -> Part:
        """Get a part by name.
        
        Args:
            name: Part name
            
        Returns:
            Part object
            
        Raises:
            KeyError: If part not found
        """
        return self._parts[name]
    
    def parts(self) -> dict[str, Part]:
        """Get all parts.
        
        Returns:
            Dictionary mapping part names to Part objects
        """
        return self._parts.copy()
    
    def add_constraint(
        self,
        constraint_type: str | ConstraintType,
        part1: str,
        part2: str,
        **parameters: Any,
    ) -> None:
        """Add a constraint between parts.
        
        Args:
            constraint_type: Type of constraint
            part1: Name of first part
            part2: Name of second part
            **parameters: Constraint-specific parameters
            
        Raises:
            ValueError: If parts don't exist
        """
        if part1 not in self._parts:
            raise ValueError(f"Part '{part1}' not found")
        if part2 not in self._parts:
            raise ValueError(f"Part '{part2}' not found")
        
        if isinstance(constraint_type, str):
            constraint_type = ConstraintType(constraint_type)
        
        self._constraints.append(
            Constraint(
                type=constraint_type,
                part1=part1,
                part2=part2,
                parameters=parameters,
            )
        )
    
    def constraints(self) -> list[Constraint]:
        """Get all constraints.
        
        Returns:
            List of Constraint objects
        """
        return self._constraints.copy()
    
    def solve(self) -> None:
        """Solve assembly constraints.
        
        Updates part positions and rotations to satisfy constraints.
        
        Raises:
            ConstraintError: If constraints cannot be satisfied
        """
        # Constraint solving implementation
        # This is a placeholder - actual implementation would use
        # numerical solver or constraint propagation
        pass
    
    def as_geometry(self) -> Geometry:
        """Get the complete assembly as a single geometry.
        
        Returns:
            Union of all transformed parts
        """
        import marimocad as mc
        
        if not self._parts:
            raise ValueError("Assembly is empty")
        
        geometries = [part.transform() for part in self._parts.values()]
        return mc.union(*geometries)
```

## Selection Data Structures

### Selector

```python
from typing import Callable, TypeVar

T = TypeVar("T", bound=Geometry)

class Selector:
    """Base class for geometry element selection.
    
    Provides filtering, sorting, and grouping of geometry elements.
    """
    
    def __init__(self, elements: list[T]) -> None:
        """Initialize selector with elements.
        
        Args:
            elements: List of geometry elements
        """
        self._elements = elements
    
    def filter(self, predicate: Callable[[T], bool]) -> "Selector[T]":
        """Filter elements by predicate.
        
        Args:
            predicate: Function returning True for elements to keep
            
        Returns:
            New selector with filtered elements
        """
        return Selector([e for e in self._elements if predicate(e)])
    
    def sort_by(
        self,
        key: str | Callable[[T], float],
        reverse: bool = False,
    ) -> "Selector[T]":
        """Sort elements by key.
        
        Args:
            key: Sort key (">Z", "<X", etc.) or callable
            reverse: Reverse sort order
            
        Returns:
            New selector with sorted elements
        """
        if isinstance(key, str):
            key = self._parse_key(key)
        
        elements = sorted(self._elements, key=key, reverse=reverse)
        return Selector(elements)
    
    def group_by(
        self,
        key: str | Callable[[T], Any],
    ) -> dict[Any, "Selector[T]"]:
        """Group elements by key.
        
        Args:
            key: Grouping key or callable
            
        Returns:
            Dictionary mapping keys to selectors
        """
        from collections import defaultdict
        
        if isinstance(key, str):
            key = self._parse_key(key)
        
        groups: dict[Any, list[T]] = defaultdict(list)
        for element in self._elements:
            groups[key(element)].append(element)
        
        return {k: Selector(v) for k, v in groups.items()}
    
    def first(self) -> T | None:
        """Get first element."""
        return self._elements[0] if self._elements else None
    
    def last(self) -> T | None:
        """Get last element."""
        return self._elements[-1] if self._elements else None
    
    def all(self) -> list[T]:
        """Get all elements."""
        return self._elements.copy()
    
    def __len__(self) -> int:
        """Get number of elements."""
        return len(self._elements)
    
    def __getitem__(self, index: int) -> T:
        """Get element by index."""
        return self._elements[index]
    
    def _parse_key(self, key_str: str) -> Callable[[T], float]:
        """Parse string key like '>Z' into callable."""
        # Implementation parses axis selectors
        pass
```

## Cache Data Structures

### CacheKey

```python
from typing import Hashable

@dataclass(frozen=True)
class CacheKey:
    """Key for geometry cache.
    
    Immutable key combining operation and parameters.
    
    Attributes:
        operation: Operation name
        parameters: Tuple of hashable parameters
    """
    
    operation: str
    parameters: tuple[Hashable, ...]
    
    @classmethod
    def from_call(
        cls,
        operation: str,
        *args: Any,
        **kwargs: Any,
    ) -> "CacheKey":
        """Create cache key from function call.
        
        Args:
            operation: Operation name
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            CacheKey instance
        """
        # Convert args and kwargs to hashable tuple
        params = []
        params.extend(cls._make_hashable(arg) for arg in args)
        params.extend(
            (k, cls._make_hashable(v))
            for k, v in sorted(kwargs.items())
        )
        return cls(operation=operation, parameters=tuple(params))
    
    @staticmethod
    def _make_hashable(value: Any) -> Hashable:
        """Convert value to hashable form."""
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        if isinstance(value, (list, tuple)):
            return tuple(CacheKey._make_hashable(v) for v in value)
        if isinstance(value, dict):
            return tuple(
                (k, CacheKey._make_hashable(v))
                for k, v in sorted(value.items())
            )
        # For geometry objects, use id
        return id(value)
```

### GeometryCache

```python
from typing import Generic

class GeometryCache(Generic[T]):
    """LRU cache for geometry objects.
    
    Caches computed geometries to avoid recomputation.
    
    Attributes:
        max_size: Maximum cache size
        cache: Ordered dictionary for LRU
    """
    
    def __init__(self, max_size: int = 1000) -> None:
        """Initialize cache.
        
        Args:
            max_size: Maximum number of cached items
        """
        from collections import OrderedDict
        
        self.max_size = max_size
        self._cache: OrderedDict[CacheKey, T] = OrderedDict()
    
    def get(self, key: CacheKey) -> T | None:
        """Get cached value.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if key in self._cache:
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]
        return None
    
    def set(self, key: CacheKey, value: T) -> None:
        """Set cached value.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        
        # Evict oldest if over max size
        if len(self._cache) > self.max_size:
            self._cache.popitem(last=False)
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)
```

## Export/Import Data Structures

### ExportFormat

```python
from enum import Enum

class ExportFormat(Enum):
    """Supported export formats."""
    
    STEP = "step"
    STL = "stl"
    SVG = "svg"
    DXF = "dxf"
    OBJ = "obj"
    GLTF = "gltf"
    
    @property
    def extensions(self) -> list[str]:
        """Get valid file extensions for format."""
        return {
            ExportFormat.STEP: [".step", ".stp"],
            ExportFormat.STL: [".stl"],
            ExportFormat.SVG: [".svg"],
            ExportFormat.DXF: [".dxf"],
            ExportFormat.OBJ: [".obj"],
            ExportFormat.GLTF: [".gltf", ".glb"],
        }[self]
```

### ExportOptions

```python
@dataclass
class ExportOptions:
    """Options for geometry export.
    
    Attributes:
        format: Export format
        linear_deflection: Mesh linear deflection (for STL, etc.)
        angular_deflection: Mesh angular deflection in degrees
        quality: Overall quality setting (low/medium/high)
        units: Unit system (mm, cm, m, in, ft)
    """
    
    format: ExportFormat
    linear_deflection: float = 0.1
    angular_deflection: float = 0.5
    quality: str = "medium"
    units: str = "mm"
```

## Summary

The data structures in marimocad are designed to:

1. **Be flexible**: Protocol-based types work with multiple backends
2. **Be type-safe**: Full type hints for IDE support
3. **Be efficient**: Caching and lazy evaluation support
4. **Be Pythonic**: Use dataclasses, protocols, enums appropriately
5. **Be extensible**: Easy to add new types and operations

These structures provide a solid foundation for the marimocad implementation while maintaining compatibility with Build123d and other backends.

---

**Document Version**: 1.0
**Last Updated**: 2024-12-15
**Status**: Approved for Implementation
