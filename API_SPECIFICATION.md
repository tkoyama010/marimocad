# marimocad API Specification

## Version: 0.1.0-dev

## Overview

This document defines the API specification for marimocad, a CAD library for Marimo notebooks. The API is designed to provide a Pythonic, reactive interface for parametric 3D modeling that leverages Marimo's reactive programming model.

## Design Principles

1. **Reactive by Default**: All geometry operations integrate seamlessly with Marimo's reactivity
2. **Pythonic API**: Clean, intuitive interface following Python best practices
3. **Type Safety**: Full type hints for improved IDE support and error detection
4. **Progressive Disclosure**: Simple tasks are simple; complex tasks are possible
5. **Backend Agnostic**: Abstract interface with Build123d as primary backend
6. **Composable**: Operations can be combined and reused
7. **Performance**: Efficient operations suitable for interactive modeling

## Core Modules

### 1. `marimocad.geometry` - Geometry Creation

#### 1.1 Primitive Shapes

```python
# 3D Primitives
def box(
    length: float,
    width: float,
    height: float,
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
        >>> box = mc.box(10, 20, 5)
        >>> centered_box = mc.box(10, 10, 10, center=True)
    """

def sphere(radius: float, center: bool = True) -> Solid:
    """Create a sphere.

    Args:
        radius: Sphere radius
        center: Center the sphere at origin if True

    Returns:
        A solid sphere geometry

    Example:
        >>> sphere = mc.sphere(5.0)
    """

def cylinder(
    radius: float,
    height: float,
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
        >>> cyl = mc.cylinder(3, 10)
    """

def cone(
    radius: float,
    height: float,
    top_radius: float = 0.0,
    center: bool = False,
) -> Solid:
    """Create a cone or frustum.

    Args:
        radius: Bottom radius
        height: Cone height along Z axis
        top_radius: Top radius (0 for cone, >0 for frustum)
        center: Center the cone at origin if True

    Returns:
        A solid cone geometry

    Example:
        >>> cone = mc.cone(5, 10)
        >>> frustum = mc.cone(5, 10, top_radius=2)
    """

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
        >>> torus = mc.torus(10, 2)
    """
```

#### 1.2 2D Shapes (for extrusion/revolution)

```python
def circle(radius: float) -> Face:
    """Create a circular face.

    Args:
        radius: Circle radius

    Returns:
        A circular face
    """

def rectangle(width: float, height: float) -> Face:
    """Create a rectangular face.

    Args:
        width: Rectangle width
        height: Rectangle height

    Returns:
        A rectangular face
    """

def polygon(points: list[tuple[float, float]]) -> Face:
    """Create a polygon from points.

    Args:
        points: List of (x, y) coordinate tuples

    Returns:
        A polygonal face
    """

def text(
    text: str,
    font_size: float = 12,
    font: str = "Arial",
) -> Face:
    """Create text as 2D geometry.

    Args:
        text: Text string to render
        font_size: Size of the font
        font: Font family name

    Returns:
        Text as a face geometry
    """
```

### 2. `marimocad.operations` - Transformations and Boolean Operations

#### 2.1 Transformations

```python
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
        >>> box = mc.box(10, 10, 10)
        >>> moved = mc.translate(box, x=5, y=10)
    """

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
        >>> box = mc.box(10, 10, 10)
        >>> rotated = mc.rotate(box, 45, axis="Z")
    """

def scale(
    geom: Geometry,
    factor: float | tuple[float, float, float],
    center: tuple[float, float, float] | None = None,
) -> Geometry:
    """Scale geometry uniformly or non-uniformly.

    Args:
        geom: Geometry to scale
        factor: Scale factor (uniform) or (x, y, z) factors
        center: Center of scaling (origin if None)

    Returns:
        Scaled geometry

    Example:
        >>> box = mc.box(10, 10, 10)
        >>> bigger = mc.scale(box, 2.0)
        >>> stretched = mc.scale(box, (1, 2, 0.5))
    """

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
    """
```

#### 2.2 Boolean Operations

```python
def union(*geoms: Geometry) -> Geometry:
    """Combine geometries (logical OR).

    Args:
        *geoms: Geometries to union

    Returns:
        Combined geometry

    Example:
        >>> box1 = mc.box(10, 10, 10)
        >>> box2 = mc.translate(mc.box(10, 10, 10), x=5)
        >>> combined = mc.union(box1, box2)
    """

def subtract(base: Geometry, *tools: Geometry) -> Geometry:
    """Subtract tool geometries from base (logical difference).

    Args:
        base: Base geometry
        *tools: Geometries to subtract

    Returns:
        Result geometry with tools removed

    Example:
        >>> box = mc.box(20, 20, 10)
        >>> cyl = mc.cylinder(3, 15)
        >>> result = mc.subtract(box, cyl)
    """

def intersect(*geoms: Geometry) -> Geometry:
    """Intersect geometries (logical AND).

    Args:
        *geoms: Geometries to intersect

    Returns:
        Intersection geometry
    """
```

#### 2.3 Modifications

```python
def fillet(
    geom: Geometry,
    radius: float,
    edges: list[Edge] | None = None,
) -> Geometry:
    """Add fillets to edges.

    Args:
        geom: Geometry to fillet
        radius: Fillet radius
        edges: Specific edges to fillet (all if None)

    Returns:
        Filleted geometry

    Example:
        >>> box = mc.box(10, 10, 10)
        >>> rounded = mc.fillet(box, 1.0)
    """

def chamfer(
    geom: Geometry,
    distance: float,
    edges: list[Edge] | None = None,
) -> Geometry:
    """Add chamfers to edges.

    Args:
        geom: Geometry to chamfer
        distance: Chamfer distance
        edges: Specific edges to chamfer (all if None)

    Returns:
        Chamfered geometry
    """

def shell(
    geom: Solid,
    thickness: float,
    faces: list[Face] | None = None,
) -> Solid:
    """Create a hollow shell.

    Args:
        geom: Solid to shell
        thickness: Wall thickness
        faces: Faces to remove (all if None)

    Returns:
        Hollowed solid
    """

def offset(
    geom: Geometry,
    distance: float,
) -> Geometry:
    """Offset geometry by distance.

    Args:
        geom: Geometry to offset
        distance: Offset distance (positive = outward)

    Returns:
        Offset geometry
    """
```

#### 2.4 Extrusion and Revolution

```python
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
        >>> circle = mc.circle(5)
        >>> cylinder = mc.extrude(circle, 10)
    """

def revolve(
    face: Face,
    angle: float = 360,
    axis: str | tuple[float, float, float] = "Z",
) -> Solid:
    """Revolve a 2D face around an axis.

    Args:
        face: Face to revolve
        angle: Revolution angle in degrees
        axis: Revolution axis

    Returns:
        Revolved solid

    Example:
        >>> profile = mc.rectangle(5, 10)
        >>> bottle = mc.revolve(profile, 360)
    """

def loft(
    faces: list[Face],
    ruled: bool = False,
) -> Solid:
    """Create a solid by lofting through faces.

    Args:
        faces: Ordered list of faces to loft through
        ruled: Use ruled surface if True

    Returns:
        Lofted solid
    """

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
    """
```

### 3. `marimocad.selectors` - Topology Selection

```python
class Selector:
    """Base class for geometry element selection."""

    def filter_by_axis(self, axis: str) -> list[Geometry]:
        """Filter elements parallel to axis."""

    def sort_by(self, key: str | Callable) -> list[Geometry]:
        """Sort elements by key."""

    def group_by(self, key: str | Callable) -> dict[Any, list[Geometry]]:
        """Group elements by key."""

def select_faces(
    geom: Geometry,
    selector: str | Callable | None = None,
) -> list[Face]:
    """Select faces from geometry.

    Args:
        geom: Geometry to select from
        selector: Selection criteria (">Z", "<X", lambda, etc.)

    Returns:
        List of selected faces

    Example:
        >>> box = mc.box(10, 10, 10)
        >>> top_faces = mc.select_faces(box, ">Z")
    """

def select_edges(
    geom: Geometry,
    selector: str | Callable | None = None,
) -> list[Edge]:
    """Select edges from geometry."""

def select_vertices(
    geom: Geometry,
    selector: str | Callable | None = None,
) -> list[Vertex]:
    """Select vertices from geometry."""
```

### 4. `marimocad.components` - Pre-built Component Library

```python
# Mechanical components
def screw(
    diameter: float,
    length: float,
    thread_pitch: float,
    head_type: str = "hex",
) -> Solid:
    """Create a screw with threads.

    Args:
        diameter: Screw diameter
        length: Screw length
        thread_pitch: Thread pitch
        head_type: Head type ("hex", "flat", "pan", etc.)

    Returns:
        Screw solid
    """

def gear(
    num_teeth: int,
    module: float,
    thickness: float,
    pressure_angle: float = 20,
) -> Solid:
    """Create a spur gear.

    Args:
        num_teeth: Number of teeth
        module: Gear module
        thickness: Gear thickness
        pressure_angle: Pressure angle in degrees

    Returns:
        Gear solid
    """

def bearing(
    inner_diameter: float,
    outer_diameter: float,
    thickness: float,
) -> Solid:
    """Create a ball bearing.

    Args:
        inner_diameter: Inner race diameter
        outer_diameter: Outer race diameter
        thickness: Bearing thickness

    Returns:
        Bearing solid
    """

# Standard profiles
def i_beam(
    height: float,
    width: float,
    web_thickness: float,
    flange_thickness: float,
) -> Face:
    """Create an I-beam profile."""

def channel(
    height: float,
    width: float,
    thickness: float,
) -> Face:
    """Create a channel profile."""
```

### 5. `marimocad.assembly` - Assembly Management

```python
class Assembly:
    """Container for multi-part assemblies."""

    def __init__(self, name: str = "assembly"):
        """Create a new assembly.

        Args:
            name: Assembly name
        """

    def add_part(
        self,
        part: Geometry,
        name: str,
        position: tuple[float, float, float] = (0, 0, 0),
        rotation: tuple[float, float, float] = (0, 0, 0),
    ) -> None:
        """Add a part to the assembly.

        Args:
            part: Geometry to add
            name: Part name
            position: Part position
            rotation: Part rotation (rx, ry, rz in degrees)
        """

    def add_constraint(
        self,
        constraint_type: str,
        part1: str,
        part2: str,
        **kwargs: Any,
    ) -> None:
        """Add a constraint between parts.

        Args:
            constraint_type: Type of constraint ("mate", "align", "distance")
            part1: First part name
            part2: Second part name
            **kwargs: Constraint-specific parameters
        """

    def get_part(self, name: str) -> Geometry:
        """Get a part by name."""

    def parts(self) -> dict[str, Geometry]:
        """Get all parts."""

    def solve(self) -> None:
        """Solve assembly constraints."""
```

### 6. `marimocad.io` - Import/Export

```python
def export_step(geom: Geometry, filename: str) -> None:
    """Export geometry to STEP format.

    Args:
        geom: Geometry to export
        filename: Output filename (.step or .stp)

    Example:
        >>> box = mc.box(10, 10, 10)
        >>> mc.export_step(box, "box.step")
    """

def export_stl(
    geom: Geometry,
    filename: str,
    linear_deflection: float = 0.1,
    angular_deflection: float = 0.5,
) -> None:
    """Export geometry to STL format.

    Args:
        geom: Geometry to export
        filename: Output filename (.stl)
        linear_deflection: Linear mesh deflection
        angular_deflection: Angular mesh deflection in degrees
    """

def export_svg(
    geom: Geometry,
    filename: str,
    view: str = "top",
    width: int = 800,
    height: int = 600,
) -> None:
    """Export geometry to SVG format (2D projection).

    Args:
        geom: Geometry to export
        filename: Output filename (.svg)
        view: View direction ("top", "front", "side", "iso")
        width: Image width
        height: Image height
    """

def import_step(filename: str) -> Geometry:
    """Import geometry from STEP format.

    Args:
        filename: Input filename (.step or .stp)

    Returns:
        Imported geometry
    """

def import_stl(filename: str) -> Geometry:
    """Import geometry from STL format.

    Args:
        filename: Input filename (.stl)

    Returns:
        Imported geometry
    """
```

### 7. `marimocad.marimo` - Marimo Integration

```python
def viewer(
    geom: Geometry | None = None,
    width: int = 800,
    height: int = 600,
    projection: str = "perspective",
) -> mo.Html:
    """Create an interactive 3D viewer for Marimo.

    Args:
        geom: Geometry to display
        width: Viewer width
        height: Viewer height
        projection: Camera projection ("perspective" or "orthographic")

    Returns:
        Marimo HTML component with 3D viewer

    Example:
        >>> box = mc.box(10, 10, 10)
        >>> mc.viewer(box)
    """

class GeometryCard:
    """Marimo UI card displaying geometry properties."""

    def __init__(self, geom: Geometry):
        """Create a geometry info card.

        Args:
            geom: Geometry to display info for
        """

    def render(self) -> mo.Html:
        """Render the card."""

def parametric_model(
    func: Callable,
    params: dict[str, mo.ui.UIElement],
) -> mo.Html:
    """Create a reactive parametric model.

    Args:
        func: Function that creates geometry from parameters
        params: Dictionary of Marimo UI elements

    Returns:
        Interactive parametric model viewer

    Example:
        >>> def create_box(length, width, height):
        ...     return mc.box(length, width, height)
        >>> params = {
        ...     "length": mo.ui.slider(1, 20, value=10),
        ...     "width": mo.ui.slider(1, 20, value=10),
        ...     "height": mo.ui.slider(1, 20, value=10),
        ... }
        >>> mc.parametric_model(create_box, params)
    """
```

### 8. `marimocad.types` - Type Definitions

```python
from typing import Protocol, Union

class Geometry(Protocol):
    """Base protocol for all geometry types."""

    def bounding_box(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get bounding box as ((xmin, ymin, zmin), (xmax, ymax, zmax))."""

    def center(self) -> tuple[float, float, float]:
        """Get center point."""

    def volume(self) -> float:
        """Get volume (for solids)."""

    def area(self) -> float:
        """Get surface area."""

class Solid(Geometry):
    """3D solid geometry."""

    def faces(self) -> list[Face]:
        """Get all faces."""

    def edges(self) -> list[Edge]:
        """Get all edges."""

    def vertices(self) -> list[Vertex]:
        """Get all vertices."""

class Face(Geometry):
    """2D surface geometry."""

    def edges(self) -> list[Edge]:
        """Get boundary edges."""

    def normal(self) -> tuple[float, float, float]:
        """Get surface normal."""

class Edge(Geometry):
    """1D curve geometry."""

    def vertices(self) -> list[Vertex]:
        """Get end vertices."""

    def length(self) -> float:
        """Get edge length."""

class Vertex(Geometry):
    """0D point geometry."""

    def position(self) -> tuple[float, float, float]:
        """Get vertex position."""

class Wire(Geometry):
    """Connected sequence of edges."""

    def edges(self) -> list[Edge]:
        """Get all edges."""

    def is_closed(self) -> bool:
        """Check if wire forms a closed loop."""
```

## Usage Examples

### Example 1: Simple Parametric Box

```python
import marimo as mo
import marimocad as mc

# Create reactive parameters
length = mo.ui.slider(5, 50, value=20, label="Length")
width = mo.ui.slider(5, 50, value=15, label="Width")
height = mo.ui.slider(5, 30, value=10, label="Height")

# Create geometry reactively
def create_box():
    return mc.box(length.value, width.value, height.value)

box = create_box()

# Display with viewer
mc.viewer(box)
```

### Example 2: Box with Hole and Fillets

```python
import marimocad as mc

# Create base box
box = mc.box(30, 20, 10)

# Create hole
hole = mc.cylinder(3, 15)
hole = mc.translate(hole, x=15, y=10)

# Subtract hole from box
result = mc.subtract(box, hole)

# Add fillets
result = mc.fillet(result, 1.0)

# Export
mc.export_step(result, "part.step")
```

### Example 3: Assembly

```python
import marimocad as mc

# Create assembly
asm = mc.Assembly("robot_arm")

# Add base
base = mc.cylinder(20, 5)
asm.add_part(base, "base", position=(0, 0, 0))

# Add arm
arm = mc.box(50, 10, 8)
asm.add_part(arm, "arm", position=(25, 0, 9))

# Add constraint
asm.add_constraint("mate", "base", "arm", faces=("top", "bottom"))

# Solve and display
asm.solve()
```

### Example 4: Component Library

```python
import marimocad as mc

# Create a gear train
gear1 = mc.gear(num_teeth=20, module=2, thickness=5)
gear2 = mc.gear(num_teeth=40, module=2, thickness=5)

# Position gears
gear2 = mc.translate(gear2, x=60)

# Create assembly
train = mc.union(gear1, gear2)

mc.viewer(train)
```

## Backend Integration

### Build123d Backend (Primary)

The Build123d backend provides the implementation for all API functions. The wrapper layer translates marimocad API calls to Build123d operations while maintaining the abstract interface.

```python
# Internal implementation structure
class Build123dBackend:
    """Build123d backend implementation."""

    def create_box(self, length: float, width: float, height: float, center: bool) -> Any:
        """Implement box creation using Build123d."""
        from build123d import Box, BuildPart, Location

        with BuildPart() as part:
            if center:
                Box(length, width, height, align=(Align.CENTER, Align.CENTER, Align.CENTER))
            else:
                Box(length, width, height)

        return part.part
```

## Reactive Integration

All geometry creation and modification functions work seamlessly with Marimo's reactivity:

```python
import marimo as mo
import marimocad as mc

# When slider changes, geometry updates automatically
@mo.reactive
def box_model(length, width, height):
    return mc.box(length, width, height)

# Create reactive UI
length_slider = mo.ui.slider(1, 50, value=10)
width_slider = mo.ui.slider(1, 50, value=10)
height_slider = mo.ui.slider(1, 50, value=10)

# Geometry updates automatically when sliders change
geometry = box_model(
    length_slider.value,
    width_slider.value,
    height_slider.value,
)
```

## Error Handling

All API functions use descriptive exceptions:

```python
class MarimoCADError(Exception):
    """Base exception for marimocad errors."""

class GeometryError(MarimoCADError):
    """Raised for invalid geometry operations."""

class ExportError(MarimoCADError):
    """Raised for export failures."""

class ImportError(MarimoCADError):
    """Raised for import failures."""

class ConstraintError(MarimoCADError):
    """Raised for constraint solving failures."""
```

## Performance Considerations

1. **Lazy Evaluation**: Complex operations are deferred until needed
2. **Caching**: Geometry results are cached to avoid recomputation
3. **Incremental Updates**: Only changed parts are recalculated
4. **Batch Operations**: Multiple operations can be batched for efficiency

## Versioning and Compatibility

- **Semantic Versioning**: API follows semver (MAJOR.MINOR.PATCH)
- **Deprecation Policy**: 2 minor versions notice for breaking changes
- **Backend Versions**: Specific Build123d version requirements documented

## Future Extensions

Potential future additions to the API:

1. **Sketch API**: Constraint-based 2D sketching
2. **Analysis**: FEA integration, mass properties
3. **Animation**: Parametric animations and motion studies
4. **Optimization**: Topology optimization, generative design
5. **Cloud Integration**: Collaborative modeling, cloud rendering
6. **Material Properties**: Physical material definitions
7. **Rendering**: Photo-realistic rendering integration

## API Stability

- **Stable**: Core geometry, operations, I/O
- **Beta**: Assembly, constraints, components
- **Experimental**: Marimo UI components, viewer

---

**Document Version**: 1.0
**Last Updated**: 2024-12-15
**Status**: Draft for Review
