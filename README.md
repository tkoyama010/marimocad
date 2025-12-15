# marimocad

A modern CAD library for Python with marimo integration.

## Features

- **Primitive Shapes**: Create basic 3D geometries (box, sphere, cylinder, cone, torus)
- **Transformations**: Translate, rotate, and scale geometries
- **Boolean Operations**: Union, difference, and intersection operations
- **2D Sketching**: Create 2D profiles with the Sketch class
- **Advanced Operations**: Extrude, revolve, and sweep 2D profiles into 3D shapes
- **Type Safety**: Comprehensive error handling and validation
- **Well Tested**: >80% code coverage with extensive unit tests

## Installation

```bash
pip install marimocad
```

## Quick Start

```python
import marimocad as mc

# Create a box
my_box = mc.box(10, 20, 30)

# Create a sphere
my_sphere = mc.sphere(15)

# Transform geometries
moved_box = mc.translate(my_box, x=20, y=10)
rotated_sphere = mc.rotate(my_sphere, axis=(0, 0, 1), angle=45)

# Boolean operations
combined = mc.union(my_box, my_sphere)
difference = mc.difference(my_box, my_sphere)

# Create with sketch and extrude
sketch = mc.Sketch().circle(10).rectangle(20, 20)
extruded = mc.extrude(sketch, 30)

# Revolve a profile
profile = mc.Sketch().rectangle(5, 15, centered=False)
vase = mc.revolve(profile, angle=360)
```

## Core Functionality

### Primitives

Create basic 3D shapes:

```python
box = mc.box(length=10, width=20, height=30)
sphere = mc.sphere(radius=10)
cylinder = mc.cylinder(radius=5, height=20)
cone = mc.cone(radius1=10, radius2=5, height=20)  # Frustum
torus = mc.torus(major_radius=20, minor_radius=5)
```

### Transformations

Transform geometries in 3D space:

```python
# Translate
moved = mc.translate(geometry, x=10, y=20, z=5)

# Rotate around an axis
rotated = mc.rotate(geometry, axis=(0, 0, 1), angle=45)

# Scale
scaled = mc.scale(geometry, x=2, y=2, z=2)
```

### Boolean Operations

Combine geometries:

```python
# Union (combine)
combined = mc.union(shape1, shape2, shape3)

# Difference (subtract)
result = mc.difference(base, tool1, tool2)

# Intersection (overlap)
overlap = mc.intersection(shape1, shape2)
```

### Sketching

Create 2D profiles:

```python
sketch = mc.Sketch()
sketch.rectangle(10, 20)
sketch.circle(5)
sketch.polygon(6, 15)  # Hexagon

# Complex paths
sketch.move_to(0, 0).line(10, 0).line(0, 10).arc((0, 0), 15).close()
```

### Advanced Operations

Create 3D shapes from 2D profiles:

```python
# Extrude
cylinder = mc.extrude(mc.Sketch().circle(10), distance=20)

# Revolve
vase = mc.revolve(profile, angle=360)

# Sweep along a path
pipe = mc.sweep(profile, path)
```

## Development

```bash
# Clone the repository
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=marimocad --cov-report=term-missing

# Run linter
ruff check src/

# Run type checker
mypy src/
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
