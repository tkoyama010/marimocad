# marimocad

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

### From PyPI

Install the latest stable release:

```bash
pip install marimocad
```

### With CAD Backend

For full functionality, install with a CAD backend (Build123d recommended):

```bash
pip install marimocad build123d
```

### For Development

For testing examples and development:

```bash
pip install marimocad[dev] build123d marimo

# Optional: For visualization
pip install ocp-vscode
```

### Requirements

- Python 3.9 or higher
- marimo >= 0.1.0
- Recommended: build123d for CAD operations

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
- [x] Design API and architecture
- [ ] Implement marimocad wrapper API
- [ ] Create component library
- [ ] Add visualization integration
- [ ] Implement assembly support
- [ ] Add constraint solver
- [ ] Documentation and tutorials

## API and Architecture Documentation

Comprehensive design documentation is now available:

- **[API Specification](API_SPECIFICATION.md)** - Complete API reference with all functions and types
- **[Architecture](ARCHITECTURE.md)** - System architecture, data flow, and design patterns
- **[Design Decisions](DESIGN_DECISIONS.md)** - Rationale for key architectural choices
- **[Data Structures](DATA_STRUCTURES.md)** - Type system and core data structures
- **[Usage Examples](EXAMPLES.md)** - Comprehensive examples of API usage

These documents provide a complete blueprint for the marimocad implementation.

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
