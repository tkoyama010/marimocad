# marimocad Documentation

Welcome to the marimocad documentation! marimocad is an interactive CAD modeling library designed for use with [marimo](https://marimo.io) reactive notebooks.

## Quick Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](api/index.rst)
- [Examples Gallery](examples.md)
- [Architecture](architecture.md)
- [Contributing](../CONTRIBUTING.md)

## Installation

Install marimocad using pip:

```bash
pip install marimocad
```

Or install from source:

```bash
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad
pip install -e .
```

## Quick Start

### Basic Shapes

Create 3D geometric shapes with a simple API:

```python
import marimocad as mc

# Create shapes
box = mc.Box(width=10, height=5, depth=3)
cylinder = mc.Cylinder(radius=3, height=10)
sphere = mc.Sphere(radius=5)

# Check properties
print(f"Box volume: {box.volume()}")
print(f"Sphere surface area: {sphere.surface_area()}")
```

### Boolean Operations

Combine shapes using constructive solid geometry:

```python
import marimocad as mc

# Create shapes
box = mc.Box(width=10, height=10, depth=10)
sphere = mc.Sphere(radius=6)

# Boolean operations
union = mc.union(box, sphere)
intersection = mc.intersection(box, sphere)
difference = mc.difference(box, sphere)
```

### Transformations

Transform shapes in 3D space:

```python
import marimocad as mc

cylinder = mc.Cylinder(radius=3, height=10)

# Transform
mc.translate(cylinder, x=5, y=10, z=0)
mc.rotate(cylinder, angle=45, axis='z')
mc.scale(cylinder, factor=2.0)
```

### Interactive with marimo

Create reactive parametric models:

```python
import marimo as mo
import marimocad as mc

# Interactive controls
width = mo.ui.slider(1, 20, value=10, label="Width")
height = mo.ui.slider(1, 20, value=5, label="Height")

# Reactive model
box = mc.Box(width=width.value, height=height.value)
mo.md(f"**Volume:** {box.volume():.2f}")
```

## Documentation Contents

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
quickstart
examples
api/index
architecture
contributing
```

## Features

- 🎨 **Simple API**: Intuitive Python interface for creating 3D shapes
- 🔄 **Interactive**: Designed for marimo reactive notebooks
- 🏗️ **Composable**: Combine shapes with boolean operations
- 📐 **Transformations**: Translate, rotate, and scale shapes easily
- 📚 **Well-documented**: Comprehensive docs with examples
- 🚀 **Lightweight**: Minimal dependencies, fast performance

## Core Modules

### shapes
Basic 3D geometric shapes (Box, Cylinder, Sphere)

### operations
Boolean operations (union, intersection, difference)

### transforms
Transformation operations (translate, rotate, scale)

## Examples

Check out our comprehensive examples:

- [Basic Shapes](../examples/01_basic_shapes.py) - Creating and manipulating shapes
- [Boolean Operations](../examples/02_boolean_operations.py) - Combining shapes with CSG
- [Transformations](../examples/03_transformations.py) - Applying transformations
- [Complex Models](../examples/04_complex_model.py) - Building complete models
- [Parametric Design](../examples/05_parametric_design.py) - Interactive parametric modeling

## Getting Help

- **Documentation**: [marimocad.readthedocs.io](https://marimocad.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/tkoyama010/marimocad/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tkoyama010/marimocad/discussions)

## Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details on:

- Setting up development environment
- Code style and standards
- Testing requirements
- Pull request process

## License

marimocad is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
