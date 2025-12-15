# marimocad

A Python CAD library for parametric modeling in [Marimo](https://marimo.io) notebooks.

## Status

🔬 **Research Phase** - Currently evaluating CAD backend libraries.

## Backend Library Selection

After comprehensive research and testing, **[Build123d](https://github.com/gumyr/build123d)** has been selected as the primary backend for marimocad.

### Why Build123d?

- ✅ **Native notebook integration** - Built-in `_repr_mimebundle_()` support
- ✅ **Modern Python API** - Context managers, type hints, and Pythonic design
- ✅ **Powerful selectors** - Intuitive filtering and topology navigation
- ✅ **Multiple paradigms** - Builder, Algebra, and Direct modeling modes
- ✅ **Excellent Marimo compatibility** - Seamless reactive updates
- ✅ **Active development** - Regular updates and improvements

See [CAD_LIBRARY_COMPARISON.md](CAD_LIBRARY_COMPARISON.md) for detailed evaluation of Build123d, CadQuery, and pythonOCC.

## Research Documentation

- **[CAD Library Comparison](CAD_LIBRARY_COMPARISON.md)** - Comprehensive evaluation of CAD backends
- **[Examples](examples/)** - Proof-of-concept demonstrations
  - [Build123d POC](examples/build123d_poc.py) - Recommended approach ⭐
  - [CadQuery POC](examples/cadquery_poc.py) - Alternative backend
  - [OCP POC](examples/ocp_poc.py) - Educational comparison

## Installation (for testing examples)

```bash
pip install build123d marimo

# Optional: For visualization
pip install ocp-vscode
```

## Quick Start (POC)

```bash
# Run the Build123d proof of concept
marimo edit examples/build123d_poc.py
```

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

This project is in early research phase. Contributions welcome!

## License

TBD

## Related Projects

- [Build123d](https://github.com/gumyr/build123d) - Our chosen CAD backend
- [CadQuery](https://github.com/CadQuery/cadquery) - Alternative CAD library
- [Marimo](https://github.com/marimo-team/marimo) - Reactive Python notebooks
- [OCP](https://github.com/CadQuery/OCP) - OpenCascade Python bindings