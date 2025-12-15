# marimocad

3D visualization components for Marimo notebooks. Create interactive 3D CAD visualizations with camera controls, multiple geometries, and dynamic updates.

## Features

- 🎨 **Interactive 3D Visualization**: Built on Plotly for smooth, responsive 3D graphics
- 🎮 **Camera Controls**: Rotate, pan, and zoom with mouse/touch controls
- 🔲 **Multiple Geometries**: Display boxes, spheres, cylinders, and custom meshes
- 💡 **Lighting & Materials**: Configurable lighting and material properties
- 🎯 **Selection & Highlighting**: Hover over geometries to see names
- ⚡ **Reactive Updates**: Automatically updates when geometry changes in Marimo
- 📦 **Simple API**: Easy-to-use, chainable methods

## Installation

```bash
pip install marimocad
```

For development:

```bash
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad
pip install -e ".[dev]"
```

## Quick Start

```python
import marimo as mo
from marimocad import Viewer3D

# Create a viewer
viewer = Viewer3D(width=800, height=600)

# Add some geometries
viewer.add_box([0, 0, 0], [1, 1, 1], color="blue", name="Box 1")
viewer.add_sphere([2, 0, 0], 0.5, color="red", name="Sphere 1")
viewer.add_cylinder([0, 2, 0], 0.5, 1.5, color="green", name="Cylinder 1")

# Display in Marimo notebook
viewer.show()
```

## Usage

### Creating a Viewer

```python
from marimocad import Viewer3D

# Create a viewer with custom dimensions
viewer = Viewer3D(
    width=800,
    height=600,
    background_color="white"
)
```

### Adding Geometries

#### Box (Cuboid)

```python
viewer.add_box(
    center=[0, 0, 0],
    size=[1, 1, 1],
    color="blue",
    opacity=0.8,
    name="My Box"
)
```

#### Sphere

```python
viewer.add_sphere(
    center=[2, 0, 0],
    radius=0.5,
    color="red",
    opacity=0.8,
    resolution=20,  # Higher = smoother
    name="My Sphere"
)
```

#### Cylinder

```python
viewer.add_cylinder(
    center=[0, 2, 0],
    radius=0.5,
    height=1.5,
    color="green",
    opacity=0.8,
    resolution=20,
    name="My Cylinder"
)
```

#### Custom Mesh

```python
import numpy as np

# Define vertices and faces
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0.5, 1, 0],
    [0.5, 0.5, 1]
])

faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [1, 2, 3],
    [2, 0, 3]
])

viewer.add_mesh(vertices, faces, color="purple", name="Tetrahedron")
```

### Camera Controls

```python
# Set camera position
viewer.set_camera(
    eye=dict(x=2, y=2, z=2),
    center=dict(x=0, y=0, z=0),
    up=dict(x=0, y=0, z=1)
)
```

### Method Chaining

All geometry methods return `self`, allowing for method chaining:

```python
viewer = (
    Viewer3D()
    .add_box([0, 0, 0], [1, 1, 1], color="blue")
    .add_sphere([2, 0, 0], 0.5, color="red")
    .add_cylinder([0, 2, 0], 0.5, 1.5, color="green")
    .set_camera(eye=dict(x=3, y=3, z=3))
    .show()
)
```

### Clearing Geometries

```python
# Clear all geometries
viewer.clear()

# Add new geometries
viewer.add_box([0, 0, 0], [2, 2, 2])
viewer.show()
```

### Using with Marimo State

```python
import marimo as mo
from marimocad import Viewer3D

# Create reactive slider
radius = mo.ui.slider(0.1, 2.0, value=0.5, step=0.1, label="Radius")

# Create viewer that updates when radius changes
def create_scene(r):
    viewer = Viewer3D()
    viewer.add_sphere([0, 0, 0], r, color="blue")
    return viewer.show()

# Display
mo.md(f"Radius: {radius.value}")
radius
create_scene(radius.value)
```

## Interactive Controls

The 3D viewer provides built-in interactive controls:

- **Rotate**: Click and drag to rotate the view
- **Pan**: Right-click and drag to pan
- **Zoom**: Scroll to zoom in/out
- **Reset**: Double-click to reset the view
- **Hover**: Hover over geometries to see their names

## API Reference

### Viewer3D

#### Constructor

```python
Viewer3D(width=800, height=600, background_color="white")
```

#### Methods

- `add_box(center, size, color, opacity, name)` - Add a box
- `add_sphere(center, radius, color, opacity, resolution, name)` - Add a sphere
- `add_cylinder(center, radius, height, color, opacity, resolution, name)` - Add a cylinder
- `add_mesh(vertices, faces, color, opacity, name)` - Add a custom mesh
- `set_camera(eye, center, up)` - Set camera position
- `clear()` - Clear all geometries
- `show()` - Display the viewer
- `to_figure()` - Get the underlying Plotly figure

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check .
```

### Building

```bash
pip install build
python -m build
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Related Projects

- [Marimo](https://github.com/marimo-team/marimo) - A reactive Python notebook
- [Plotly](https://plotly.com/python/) - Interactive graphing library