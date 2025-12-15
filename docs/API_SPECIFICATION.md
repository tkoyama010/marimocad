# marimocad API Specification

## Overview

marimocad is a reactive CAD library designed to work seamlessly with Marimo's reactive programming model. It provides a Pythonic API for creating, manipulating, and visualizing 3D CAD models with automatic updates when parameters change.

## Design Philosophy

1. **Reactive by Default**: All CAD objects are reactive and automatically update when their parameters change
2. **Pythonic API**: Context managers and object-oriented design for intuitive usage
3. **Type-Safe**: Full type hints for IDE support and type checking
4. **Composable**: Easy to combine and transform geometric objects
5. **Visualization-First**: Built-in 3D visualization for Marimo notebooks

## Core API

### 1. Geometry Creation

#### Basic Primitives

```python
from marimocad import primitives

# 2D Shapes
circle = primitives.circle(radius=10.0)
rectangle = primitives.rectangle(width=20.0, height=10.0)
polygon = primitives.polygon(points=[(0,0), (10,0), (10,10), (0,10)])
ellipse = primitives.ellipse(major=15.0, minor=10.0)

# 3D Shapes
box = primitives.box(width=10.0, height=10.0, depth=10.0)
sphere = primitives.sphere(radius=5.0)
cylinder = primitives.cylinder(radius=5.0, height=10.0)
cone = primitives.cone(radius=5.0, height=10.0)
torus = primitives.torus(major_radius=10.0, minor_radius=2.0)
```

#### Sketch-Based Modeling

```python
from marimocad import Sketch, BuildPart

# Create a 2D sketch
with Sketch() as sketch:
    sketch.add_circle(center=(0, 0), radius=10)
    sketch.add_rectangle(center=(20, 0), width=15, height=10)
    
# Extrude sketch to create 3D part
part = sketch.extrude(distance=5.0)

# Alternative: Context-based part building
with BuildPart() as part:
    with Sketch(plane="XY") as profile:
        profile.add_rectangle(width=30, height=20)
    part.extrude(distance=10)
    part.fillet(edges=part.edges(), radius=2.0)
```

#### Advanced Geometry

```python
from marimocad import spline, loft, sweep

# NURBS curves and surfaces
curve = spline(points=[(0,0,0), (5,5,5), (10,0,0)], degree=3)

# Lofting between profiles
profile1 = primitives.circle(radius=10.0)
profile2 = primitives.circle(radius=5.0).translate(z=20)
lofted = loft([profile1, profile2])

# Sweeping along a path
path = spline(points=[(0,0,0), (10,10,0), (20,0,0)])
profile = primitives.circle(radius=2.0)
swept = sweep(profile=profile, path=path)
```

### 2. Transformations

All transformations return new objects (immutable) to maintain reactivity:

```python
from marimocad import primitives

box = primitives.box(10, 10, 10)

# Basic transformations
translated = box.translate(x=5, y=0, z=0)
rotated = box.rotate(axis="Z", angle=45)  # angle in degrees
scaled = box.scale(x=2, y=1, z=1)
mirrored = box.mirror(plane="XY")

# Chaining transformations
transformed = box.translate(x=10).rotate(axis="Z", angle=45).scale(2)

# Matrix-based transformation
import numpy as np
matrix = np.array([[1, 0, 0, 5],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
transformed = box.transform(matrix)
```

### 3. Boolean Operations

```python
from marimocad import primitives

box1 = primitives.box(20, 20, 20)
box2 = primitives.box(10, 10, 30).translate(x=5, y=5, z=-5)

# Boolean operations
union = box1 + box2  # or box1.union(box2)
difference = box1 - box2  # or box1.subtract(box2)
intersection = box1 & box2  # or box1.intersect(box2)

# Multiple operations
result = (box1 + box2) - primitives.sphere(radius=5)
```

### 4. Modification Operations

```python
from marimocad import primitives

box = primitives.box(30, 20, 10)

# Filleting and chamfering
filleted = box.fillet(edges=box.edges(), radius=2.0)
chamfered = box.chamfer(edges=box.edges(), distance=1.5)

# Shelling
shelled = box.shell(faces=box.faces(">Z"), thickness=2.0)

# Offsetting
offset = box.offset(distance=2.0)

# Edge/Face selection
top_edges = box.edges(">Z")  # Edges facing upward
side_faces = box.faces("|X")  # Faces parallel to X axis
all_edges = box.edges()
```

### 5. Measurement and Queries

```python
from marimocad import primitives

box = primitives.box(10, 20, 30)

# Geometric properties
volume = box.volume
surface_area = box.surface_area
center = box.center_of_mass
bounding_box = box.bounding_box

# Topological queries
num_faces = len(box.faces())
num_edges = len(box.edges())
num_vertices = len(box.vertices())

# Distance and intersection
distance = box.distance_to(other_shape)
intersects = box.intersects(other_shape)
```

## Marimo Integration

### Reactive Parameters

```python
import marimo as mo
from marimocad import primitives, visualize

# Create reactive sliders
radius = mo.ui.slider(1, 20, value=10, label="Radius")
height = mo.ui.slider(5, 50, value=20, label="Height")

# Create reactive CAD model
cylinder = primitives.cylinder(radius=radius.value, height=height.value)

# Visualize (automatically updates when sliders change)
viewer = visualize(cylinder)
mo.vstack([radius, height, viewer])
```

### Component-Based Modeling

```python
import marimo as mo
from marimocad import Component, primitives

class FlangeBolt(Component):
    """Parametric flange bolt component."""
    
    def __init__(self, diameter, length, head_height):
        super().__init__()
        self.diameter = diameter
        self.length = length
        self.head_height = head_height
    
    def build(self):
        # Shaft
        shaft = primitives.cylinder(
            radius=self.diameter / 2,
            height=self.length
        )
        
        # Head
        head = primitives.cylinder(
            radius=self.diameter,
            height=self.head_height
        ).translate(z=self.length)
        
        return shaft + head

# Usage in Marimo
diameter = mo.ui.slider(4, 12, value=8)
bolt = FlangeBolt(diameter=diameter.value, length=50, head_height=5)
mo.ui.show(bolt.render())
```

### Assembly Management

```python
from marimocad import Assembly, primitives

# Create an assembly
assembly = Assembly(name="motor_mount")

# Add parts with constraints
base_plate = primitives.box(100, 100, 10)
assembly.add_part("base", base_plate, position=(0, 0, 0))

mount = primitives.box(30, 30, 40)
assembly.add_part("mount", mount, position=(35, 35, 10))

# Export assembly
assembly.save("motor_mount.step")

# Visualize
viewer = assembly.visualize()
```

## 3D Visualization

### Basic Visualization

```python
from marimocad import primitives, visualize

box = primitives.box(10, 10, 10)

# Default visualization
viewer = visualize(box)

# With options
viewer = visualize(
    box,
    color="#FF6B6B",
    opacity=0.8,
    show_edges=True,
    edge_color="#000000",
    background="#FFFFFF"
)

# Multiple objects
viewer = visualize([box, sphere, cylinder])
```

### Interactive Viewer

```python
from marimocad import InteractiveViewer, primitives

box = primitives.box(10, 10, 10)

# Create interactive viewer with controls
viewer = InteractiveViewer(
    objects=[box],
    enable_rotation=True,
    enable_zoom=True,
    enable_pan=True,
    show_grid=True,
    show_axes=True
)

# Export as HTML for sharing
viewer.export_html("model.html")
```

## Data Structures

### Shape Base Class

```python
class Shape:
    """Base class for all geometric shapes."""
    
    @property
    def volume(self) -> float: ...
    
    @property
    def surface_area(self) -> float: ...
    
    @property
    def center_of_mass(self) -> tuple[float, float, float]: ...
    
    @property
    def bounding_box(self) -> BoundingBox: ...
    
    def translate(self, x: float = 0, y: float = 0, z: float = 0) -> 'Shape': ...
    
    def rotate(self, axis: str, angle: float) -> 'Shape': ...
    
    def scale(self, x: float = 1, y: float = 1, z: float = 1) -> 'Shape': ...
    
    def union(self, other: 'Shape') -> 'Shape': ...
    
    def subtract(self, other: 'Shape') -> 'Shape': ...
    
    def intersect(self, other: 'Shape') -> 'Shape': ...
```

### Specialized Shape Classes

```python
class Shape2D(Shape):
    """Base class for 2D shapes."""
    
    def extrude(self, distance: float) -> 'Shape3D': ...
    
    def revolve(self, axis: str = "Z", angle: float = 360) -> 'Shape3D': ...

class Shape3D(Shape):
    """Base class for 3D shapes."""
    
    def faces(self, selector: str = "") -> list[Face]: ...
    
    def edges(self, selector: str = "") -> list[Edge]: ...
    
    def vertices(self, selector: str = "") -> list[Vertex]: ...
    
    def fillet(self, edges: list[Edge], radius: float) -> 'Shape3D': ...
    
    def chamfer(self, edges: list[Edge], distance: float) -> 'Shape3D': ...
    
    def shell(self, faces: list[Face], thickness: float) -> 'Shape3D': ...
```

## File I/O

### Import

```python
from marimocad import io

# Import various CAD formats
shape = io.import_step("model.step")
shape = io.import_stl("model.stl")
shape = io.import_obj("model.obj")
shape = io.import_iges("model.iges")

# Import with options
shape = io.import_step("model.step", heal=True, scale=1.0)
```

### Export

```python
from marimocad import io, primitives

box = primitives.box(10, 10, 10)

# Export various CAD formats
io.export_step(box, "box.step")
io.export_stl(box, "box.stl", linear_deflection=0.1)
io.export_obj(box, "box.obj")
io.export_iges(box, "box.iges")
io.export_gltf(box, "box.gltf")

# Export with options
io.export_stl(
    box,
    "box.stl",
    linear_deflection=0.01,  # Mesh quality
    angular_deflection=0.5,
    ascii=False
)

# Export assembly
assembly.export_step("assembly.step")
```

### Serialization

```python
from marimocad import io

# Save/load native format (for session persistence)
box.save_native("box.mcad")
loaded_box = io.load_native("box.mcad")

# JSON serialization for parameter storage
params = box.to_dict()
restored_box = primitives.from_dict(params)
```

## Error Handling

```python
from marimocad.exceptions import (
    GeometryError,
    InvalidOperationError,
    VisualizationError,
    ImportError,
    ExportError
)

try:
    result = box1 - box2
except InvalidOperationError as e:
    print(f"Boolean operation failed: {e}")

try:
    shape = io.import_step("missing.step")
except ImportError as e:
    print(f"Import failed: {e}")
```

## Type Hints

All functions include complete type hints:

```python
from typing import Union, Optional, Sequence
from marimocad.types import Vector3, Matrix4x4, Color

def box(
    width: float,
    height: float,
    depth: float,
    center: bool = True
) -> Shape3D: ...

def translate(
    shape: Shape,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0
) -> Shape: ...

def visualize(
    shapes: Union[Shape, Sequence[Shape]],
    color: Optional[Color] = None,
    opacity: float = 1.0,
    **kwargs
) -> Viewer: ...
```

## Performance Considerations

1. **Lazy Evaluation**: Complex operations are computed only when needed
2. **Caching**: Results are cached to avoid redundant computations
3. **Batch Operations**: Multiple modifications can be batched for efficiency
4. **Progressive Rendering**: Large models render progressively in visualization

## Future Extensions

1. **Parametric Constraints**: Geometric and dimensional constraints
2. **Sketch Constraints**: Tangent, perpendicular, equal length, etc.
3. **FEA Integration**: Basic finite element analysis capabilities
4. **G-code Generation**: For CNC machining and 3D printing
5. **Animation**: Time-based parametric animations
6. **Collaborative Editing**: Real-time multi-user CAD sessions

## Version History

- **v0.1.0** (Planned): Initial API specification
