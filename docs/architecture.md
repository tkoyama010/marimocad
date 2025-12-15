# marimocad Architecture

This document describes the architecture and design principles of marimocad.

## Overview

marimocad is designed as a lightweight, Pythonic CAD library optimized for use in interactive marimo notebooks. The architecture emphasizes simplicity, composability, and extensibility.

## Design Principles

### 1. Simplicity First
- Intuitive API that follows Python conventions
- Minimal learning curve for users familiar with Python
- Clear, readable code over clever abstractions

### 2. Composability
- Shapes are first-class objects that can be easily combined
- Operations return new shapes that can be further transformed
- Support for complex models through simple building blocks

### 3. Type Safety
- Full type hints throughout the codebase
- Better IDE support and autocomplete
- Catch errors at development time

### 4. Interactivity
- Designed for reactive notebooks (marimo)
- Fast execution for real-time parameter updates
- Minimal state management complexity

### 5. Extensibility
- Easy to add new shapes and operations
- Plugin-friendly architecture
- Clear extension points

## System Architecture

```
marimocad/
├── shapes.py       # Basic geometric shapes
├── operations.py   # Boolean operations (CSG)
├── transforms.py   # Transformation operations
└── __init__.py     # Public API exports
```

### Component Diagram

```
┌─────────────────────────────────────────┐
│           marimocad Library             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌────────────┐          │
│  │  Shapes  │  │ Operations │          │
│  ├──────────┤  ├────────────┤          │
│  │ • Box    │  │ • Union    │          │
│  │ • Cylinder  │ • Intersect│          │
│  │ • Sphere │  │ • Difference│         │
│  └──────────┘  └────────────┘          │
│                                         │
│  ┌────────────────────────┐            │
│  │    Transforms          │            │
│  ├────────────────────────┤            │
│  │ • translate            │            │
│  │ • rotate               │            │
│  │ • scale                │            │
│  │ • mirror               │            │
│  └────────────────────────┘            │
│                                         │
└─────────────────────────────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  marimo notebook │
        │  (User Interface)│
        └──────────────────┘
```

## Core Components

### 1. Shapes Module

**Purpose**: Define basic 3D geometric shapes

**Key Classes**:
- `Shape`: Abstract base class for all shapes
- `Box`: Rectangular cuboid
- `Cylinder`: Cylindrical shape
- `Sphere`: Spherical shape

**Design**:
- Each shape is an immutable data structure (conceptually)
- Shapes know how to calculate their own properties (volume, surface area)
- Shapes maintain their position in 3D space
- Bounding box calculation for spatial queries

**Example**:
```python
class Shape:
    def __init__(self, name: str = "") -> None:
        self.position = np.array([0.0, 0.0, 0.0])
        self.name = name
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError()
```

### 2. Operations Module

**Purpose**: Implement Constructive Solid Geometry (CSG) operations

**Key Classes**:
- `Operation`: Base class for boolean operations
- `Union`: Combines multiple shapes
- `Intersection`: Finds common volume
- `Difference`: Subtracts shapes

**Design**:
- Operations are themselves shapes (composite pattern)
- Lazy evaluation - operations store references to operands
- Tree structure for complex operations

**Example**:
```python
class Union(Operation):
    def __init__(self, *shapes: Shape, name: str = "") -> None:
        self.shapes = list(shapes)
    
    def get_bounds(self) -> tuple:
        # Calculate bounding box of all shapes
        ...
```

### 3. Transforms Module

**Purpose**: Provide transformation operations

**Key Functions**:
- `translate()`: Move shapes in space
- `rotate()`: Rotate around axes
- `scale()`: Resize shapes
- `mirror()`: Reflect across planes

**Design**:
- Transforms modify shapes in-place for efficiency
- Chainable operations for fluent API
- Support both simple and complex transformations

**Example**:
```python
def translate(shape: Shape, x: float = 0, y: float = 0, z: float = 0) -> Shape:
    shape.position += np.array([x, y, z])
    return shape
```

## Data Flow

### Creating and Transforming Shapes

```
User Code
    │
    ▼
Create Shape (Box, Cylinder, etc.)
    │
    ▼
Apply Transformations (translate, rotate, scale)
    │
    ▼
Combine with Operations (union, difference, etc.)
    │
    ▼
Final Model
```

### Example Flow

```python
# 1. Create shapes
box = Box(width=10, height=10, depth=10)
sphere = Sphere(radius=6)

# 2. Transform
translate(sphere, x=5, y=5, z=0)

# 3. Combine
result = difference(box, sphere)

# 4. Query
volume = result.base.volume()  # Access base shape
bounds = result.get_bounds()   # Get bounding box
```

## Design Patterns

### 1. Composite Pattern
Operations can contain other operations, creating a tree structure:

```python
# Nested operations
outer = union(
    box1,
    difference(
        box2,
        sphere
    )
)
```

### 2. Builder Pattern
Shapes are built incrementally:

```python
box = Box(width=10, height=5, depth=3)
translate(box, x=10, y=5)
rotate(box, angle=45, axis='z')
```

### 3. Strategy Pattern
Different shapes implement the same interface differently:

```python
class Shape:
    def volume(self) -> float:
        raise NotImplementedError()

class Box(Shape):
    def volume(self) -> float:
        return self.width * self.height * self.depth

class Sphere(Shape):
    def volume(self) -> float:
        return (4/3) * pi * self.radius**3
```

## Integration with marimo

### Reactive Execution

marimocad is designed to work seamlessly with marimo's reactive execution model:

```python
import marimo as mo
import marimocad as mc

# Create reactive UI elements
width = mo.ui.slider(1, 20, value=10)
height = mo.ui.slider(1, 20, value=5)

# Create shape that updates reactively
box = mc.Box(width=width.value, height=height.value)
mo.md(f"Volume: {box.volume()}")
```

When sliders change, marimo automatically:
1. Re-executes cells that depend on the slider values
2. Creates a new box with updated dimensions
3. Recalculates and displays the volume

### Performance Considerations

- Shapes are lightweight objects (just store parameters)
- Transformations are fast (simple arithmetic)
- No expensive rendering in the core library
- Defer computation until needed

## Extension Points

### Adding New Shapes

To add a new shape:

1. Inherit from `Shape` base class
2. Implement required methods (`get_bounds()`, etc.)
3. Add shape-specific properties and methods
4. Export from `__init__.py`

Example:
```python
class Cone(Shape):
    def __init__(self, radius: float, height: float, name: str = "") -> None:
        super().__init__(name)
        self.radius = radius
        self.height = height
    
    def volume(self) -> float:
        return (1/3) * np.pi * self.radius**2 * self.height
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        # Implement bounding box calculation
        ...
```

### Adding New Operations

To add a new operation:

1. Inherit from `Operation` base class
2. Implement operation-specific logic
3. Add convenience function
4. Export from `__init__.py`

### Adding New Transforms

To add a new transform:

1. Create a function that modifies shapes
2. Follow the same signature pattern
3. Return the modified shape
4. Export from `__init__.py`

## Future Architecture Considerations

### Planned Features

1. **Mesh Export**
   - Add `export()` methods to shapes
   - Support STL, OBJ formats
   - Implement mesh generation algorithms

2. **Visualization**
   - Integration with plotly or three.js
   - Real-time 3D preview in notebooks
   - Interactive manipulation

3. **Advanced CSG**
   - Offset operations
   - Shell/hollow operations
   - Fillet and chamfer

4. **2D Shapes**
   - Extend architecture to support 2D
   - Extrusion operations
   - 2D to 3D conversion

5. **Performance Optimization**
   - Spatial indexing for complex models
   - GPU acceleration for mesh operations
   - Caching of computed results

### Scalability

The current architecture supports:
- Models with hundreds of primitive shapes
- Moderate nesting of operations
- Real-time parameter updates in notebooks

For very large models:
- Consider implementing spatial partitioning
- Add lazy evaluation for operation trees
- Implement progressive rendering

## Testing Strategy

### Unit Tests
- Test each shape's volume, surface area calculations
- Test transformations modify shapes correctly
- Test operations combine shapes properly
- Test error handling for invalid inputs

### Integration Tests
- Test complex model creation
- Test interaction between components
- Test with marimo notebooks

### Performance Tests
- Benchmark shape creation
- Benchmark transformation operations
- Benchmark operation execution

## Documentation Standards

All code should include:
- Module-level docstrings
- Class docstrings with examples
- Method/function docstrings with type hints
- Inline comments for complex logic

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed standards.

## Security Considerations

Current implementation:
- No external network calls
- No file system access (except future export features)
- No code execution from user strings
- Safe numerical computations

Future considerations:
- Validate file imports carefully
- Sanitize any user-provided expressions
- Limit computational resources for complex operations

## Conclusion

marimocad's architecture prioritizes simplicity and composability while maintaining extensibility for future features. The design allows users to quickly create CAD models while providing clear paths for advanced usage and contributions.

For more information:
- [API Documentation](api/index.rst)
- [Examples](../examples/)
- [Contributing Guide](../CONTRIBUTING.md)
