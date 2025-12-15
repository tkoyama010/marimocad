# marimocad

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**marimocad** is an interactive CAD (Computer-Aided Design) modeling library for Python, designed to work seamlessly with [marimo](https://marimo.io) reactive notebooks. Create, manipulate, and visualize 3D geometric shapes with an intuitive Python API.

## ✨ Features

- 🎨 **Simple API**: Intuitive Python interface for creating 3D shapes
- 🔄 **Interactive**: Designed for marimo reactive notebooks
- 🏗️ **Composable**: Combine shapes with boolean operations (union, intersection, difference)
- 📐 **Transformations**: Translate, rotate, and scale shapes easily
- 📚 **Well-documented**: Comprehensive documentation with examples
- 🚀 **Lightweight**: Minimal dependencies, fast performance

## 📦 Installation

### From PyPI (when published)

```bash
pip install marimocad
```

### From source

```bash
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad
pip install -e .
```

### Development installation

```bash
pip install -e ".[dev,docs]"
```

## 🚀 Quick Start

### Basic Shapes

```python
import marimocad as mc

# Create basic shapes
box = mc.Box(width=10, height=5, depth=3)
cylinder = mc.Cylinder(radius=2, height=10)
sphere = mc.Sphere(radius=5)

# Check properties
print(f"Box volume: {box.volume()}")
print(f"Sphere surface area: {sphere.surface_area()}")
```

### Boolean Operations

```python
import marimocad as mc

# Create shapes
box = mc.Box(width=10, height=10, depth=10)
sphere = mc.Sphere(radius=6)

# Combine with boolean operations
union_shape = mc.union(box, sphere)
intersection_shape = mc.intersection(box, sphere)
difference_shape = mc.difference(box, sphere)
```

### Transformations

```python
import marimocad as mc

# Create and transform shapes
cylinder = mc.Cylinder(radius=3, height=10)

# Translate
mc.translate(cylinder, x=5, y=10, z=0)

# Rotate
mc.rotate(cylinder, angle=45, axis='z')

# Scale
mc.scale(cylinder, factor=2.0)
```

### Using with marimo

```python
import marimo as mo
import marimocad as mc

# Create interactive sliders
width = mo.ui.slider(1, 20, value=10, label="Width")
height = mo.ui.slider(1, 20, value=5, label="Height")
depth = mo.ui.slider(1, 20, value=3, label="Depth")

# Create reactive box
box = mc.Box(width=width.value, height=height.value, depth=depth.value)
mo.md(f"**Volume:** {box.volume():.2f} cubic units")
```

## 📖 Documentation

Full documentation is available at [marimocad.readthedocs.io](https://marimocad.readthedocs.io) (coming soon).

### Core Modules

- **shapes**: Basic 3D geometric shapes (Box, Cylinder, Sphere)
- **operations**: Boolean operations (union, intersection, difference)
- **transforms**: Transformation operations (translate, rotate, scale)

## 📚 Examples

Check out the `examples/` directory for more detailed examples:

- [01_basic_shapes.py](examples/01_basic_shapes.py) - Creating and manipulating basic shapes
- [02_boolean_operations.py](examples/02_boolean_operations.py) - Combining shapes with CSG operations
- [03_transformations.py](examples/03_transformations.py) - Applying transformations
- [04_complex_model.py](examples/04_complex_model.py) - Building complex models
- [05_parametric_design.py](examples/05_parametric_design.py) - Parametric CAD modeling

## 🏗️ Architecture

marimocad is built on these core principles:

- **Simplicity**: Easy-to-understand API with minimal learning curve
- **Composability**: Shapes and operations can be combined naturally
- **Extensibility**: Easy to add new shapes and operations
- **Type Safety**: Full type hints for better IDE support

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad

# Install in development mode with all dependencies
pip install -e ".[dev,docs]"

# Run tests
pytest

# Run linters
black src tests
ruff check src tests
mypy src
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for use with [marimo](https://marimo.io) reactive notebooks
- Inspired by OpenSCAD and other CAD tools
- Thanks to all contributors!

## 📮 Contact

- **Author**: Tetsuo Koyama
- **Email**: tkoyama010@gmail.com
- **GitHub**: [@tkoyama010](https://github.com/tkoyama010)

## 🗺️ Roadmap

- [ ] Add mesh export capabilities (STL, OBJ)
- [ ] Implement 2D shapes and operations
- [ ] Add visualization with plotly or three.js
- [ ] Support for more complex CSG operations
- [ ] Import existing CAD files
- [ ] GPU-accelerated rendering
- [ ] Integration with FEM solvers