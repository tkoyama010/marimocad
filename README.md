# marimocad

A reactive CAD library for Marimo notebooks - Design, model, and visualize 3D CAD models with the power of reactive programming.

## Overview

marimocad brings professional CAD modeling capabilities to Marimo's reactive notebook environment. Create parametric 3D models that automatically update as you adjust parameters, leveraging Marimo's reactive programming model for an intuitive and powerful design experience.

## Features

- 🎨 **Intuitive API** - Pythonic interface with primitives, transformations, and boolean operations
- ⚡ **Reactive by Default** - Models automatically update when parameters change
- 🔧 **Parametric Modeling** - Create designs that adapt to changing requirements
- 📐 **Professional CAD Operations** - Filleting, chamfering, shelling, lofting, and more
- 🏗️ **Assembly Management** - Build complex assemblies with multiple components
- 📊 **3D Visualization** - Interactive 3D viewer integrated into Marimo notebooks
- 💾 **Industry Standard Formats** - Import/export STEP, IGES, STL, OBJ, GLTF
- 🧮 **Measurements & Analysis** - Volume, surface area, center of mass, and more

## Quick Example

```python
import marimo as mo
from marimocad import primitives, visualize

# Create reactive parameters
radius = mo.ui.slider(5, 30, value=15, label="Radius")
height = mo.ui.slider(10, 50, value=30, label="Height")

# Create parametric CAD model
cylinder = primitives.cylinder(radius=radius.value, height=height.value)

# Visualize (automatically updates when sliders change)
mo.vstack([
    mo.hstack([radius, height]),
    visualize(cylinder, color="#4ECDC4")
])
```

## Documentation

Comprehensive documentation is available in the [docs](./docs) directory:

- **[API Specification](./docs/API_SPECIFICATION.md)** - Complete API reference with examples
- **[Architecture](./docs/ARCHITECTURE.md)** - System design and architecture details
- **[Design Decisions](./docs/DESIGN_DECISIONS.md)** - Rationale behind key design choices
- **[Examples](./docs/examples.py)** - 15+ comprehensive usage examples

## Installation (Planned)

```bash
pip install marimocad
```

## Current Status

🚧 **In Design Phase** - This project is currently in the design and planning phase. The API specification, architecture, and design documentation have been completed. Implementation is planned for future releases.

## Design Highlights

### Immutable & Reactive
All shapes are immutable, making them perfect for Marimo's reactive programming model. Changes create new objects, enabling automatic dependency tracking.

### Pythonic API
```python
# Method chaining for transformations
result = box.translate(x=10).rotate(axis="Z", angle=45).fillet(radius=2)

# Operator overloading for boolean operations
combined = box1 + box2 - sphere  # union and difference

# Context managers for complex construction
with BuildPart() as bracket:
    with Sketch(plane="XY") as profile:
        profile.add_rectangle(width=30, height=20)
    bracket.extrude(distance=10)
```

### Professional CAD Kernel
Built on OpenCASCADE (via OCP), providing industry-standard BREP modeling, NURBS surfaces, and advanced geometric operations.

## Roadmap

- [x] API specification and design
- [x] Architecture documentation
- [x] Example code and use cases
- [ ] Core geometry engine implementation
- [ ] Marimo integration
- [ ] 3D visualization component
- [ ] File I/O support
- [ ] Testing and validation
- [ ] Initial release (v0.1.0)

## Contributing

Contributions are welcome! This project is in early stages, and we're looking for:
- Feedback on API design
- Use case suggestions
- Implementation contributions
- Documentation improvements

## License

[To be determined]

## Acknowledgments

Inspired by:
- [Marimo](https://github.com/marimo-team/marimo) - Reactive Python notebooks
- [CadQuery](https://github.com/CadQuery/cadquery) - Python CAD scripting
- [build123d](https://github.com/gumyr/build123d) - Pythonic CAD modeling
- [OpenCASCADE](https://www.opencascade.com/) - CAD kernel

## Contact

For questions or discussions, please open an issue on GitHub.
CAD tools for marimo notebooks - Interactive 3D modeling and computational geometry.

## Status

🔬 **Research Phase** - Currently evaluating CAD backend libraries.

## Backend Library Selection

After comprehensive research and testing, **[Build123d](https://github.com/gumyr/build123d)** has been selected as the primary backend for marimocad.

### Why Build123d?

- ✅ **Native notebook integration** - Built-in `_repr_html_()` support
- ✅ **Modern Python API** - Context managers, type hints, and Pythonic design
- ✅ **Powerful selectors** - Intuitive filtering and topology navigation
- ✅ **Multiple paradigms** - Builder, Algebra, and Direct modeling modes
- ✅ **Excellent Marimo compatibility** - Seamless reactive updates
- ✅ **Active development** - Regular updates and improvements

See [CAD_LIBRARY_COMPARISON.md](CAD_LIBRARY_COMPARISON.md) for detailed evaluation of Build123d, CadQuery, and pythonOCC.

## Installation

For the package (when available):

## Installation

```bash
pip install marimocad
```

For testing examples:

```bash
pip install build123d marimo

# Optional: For visualization
pip install ocp-vscode
```

## Development

For development, clone the repository and install with development dependencies using [uv](https://docs.astral.sh/uv/) (recommended):

```bash
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad
uv sync
```

Or using pip:

```bash
git clone https://github.com/tkoyama010/marimocad.git
cd marimocad
pip install -e ".[dev]"
```

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting with a comprehensive set of rules enabled.

Run linting:
```bash
ruff check .
```

Run formatting:
```bash
ruff format .
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality before commits:

```bash
pre-commit install
```

## Research Documentation

- **[CAD Library Comparison](CAD_LIBRARY_COMPARISON.md)** - Comprehensive evaluation of CAD backends
- **[Examples](examples/)** - Proof-of-concept demonstrations
  - [Build123d POC](examples/build123d_poc.py) - Recommended approach ⭐
  - [CadQuery POC](examples/cadquery_poc.py) - Alternative backend
  - [OCP POC](examples/ocp_poc.py) - Educational comparison

## Quick Start (POC)

```bash
# Run the Build123d proof of concept
marimo edit examples/build123d_poc.py
```

## Testing

The example code is tested automatically via GitHub Actions CI. You can also run tests locally:

```bash
# Install dependencies
pip install build123d cadquery marimo

# Run tests
python tests/test_examples.py
```

See [tests/README.md](tests/README.md) for more details on testing.

## Project Goals

1. **Parametric CAD in Marimo** - Leverage Marimo's reactivity for interactive CAD modeling
2. **Pythonic API** - Clean, intuitive interface for CAD operations
3. **Component Library** - Pre-built mechanical components (screws, gears, bearings, etc.)
4. **Export Support** - STEP, STL, SVG, and other CAD formats
5. **Assembly Modeling** - Multi-part assemblies with constraints

## Roadmap

- [x] Research and evaluate CAD backend libraries
- [x] Select primary backend (Build123d)
- [x] Create proof-of-concept examples
- [ ] Implement marimocad wrapper API
- [ ] Create component library
- [ ] Add visualization integration
- [ ] Implement assembly support
- [ ] Add constraint solver
- [ ] Documentation and tutorials

## Research Findings

### Libraries Evaluated

| Library | Score | Recommendation |
|---------|-------|----------------|
| **Build123d** | 39/40 | ⭐ Primary backend |
| **CadQuery** | 38/40 | Secondary option |
| **pythonOCC/OCP** | 27/40 | Not recommended for user API |

### Performance Comparison

All libraries showed excellent performance for interactive use:

- **CadQuery**: 0.0096s average operation time
- **Build123d**: 0.0120s average operation time
- **OCP**: 0.0040s average (but requires 10-20x more code)

See the [full comparison document](CAD_LIBRARY_COMPARISON.md) for detailed analysis.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

MIT License - see LICENSE file for details.

## Related Projects

- [Build123d](https://github.com/gumyr/build123d) - Our chosen CAD backend
- [CadQuery](https://github.com/CadQuery/cadquery) - Alternative CAD library
- [Marimo](https://github.com/marimo-team/marimo) - Reactive Python notebooks
- [OCP](https://github.com/CadQuery/OCP) - OpenCascade Python bindings
