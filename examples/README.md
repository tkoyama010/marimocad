# CAD Library Proof of Concept Examples

This directory contains proof-of-concept examples demonstrating the integration of different CAD libraries with Marimo.

## 🌐 Try Online First!

**[Launch WASM Demo](https://tkoyama010.github.io/marimocad/)** - No installation required!

## Files

### 1. `wasm_demo.py` (🌐 Browser Version)
WebAssembly-optimized demo that runs entirely in the browser via Pyodide.

**Features:**
- No installation required
- Interactive reactive controls
- Real-time parameter updates
- Browser-compatible (when OCP.wasm available)
- Simplified for fast loading

**Try online:**
- **[Live Demo](https://tkoyama010.github.io/marimocad/)**

**Run locally:**
```bash
pip install marimo
marimo edit wasm_demo.py
```

**Export to WASM:**
```bash
marimo export html-wasm wasm_demo.py -o output --mode run
```

See [WASM_DEPLOYMENT.md](../WASM_DEPLOYMENT.md) for deployment guide.

### 2. `build123d_poc.py` (🖥️ RECOMMENDED ⭐)
Demonstrates Build123d integration with Marimo. This is the **recommended approach** for marimocad desktop usage.

**Features:**
- Parametric box with reactive sliders
- Complex bracket design
- Advanced selectors and filtering
- Export functionality
- Context manager API
- Full 3D rendering support

**To run:**
```bash
pip install build123d marimo
marimo edit build123d_poc.py
```

### 3. `cadquery_poc.py` (Alternative)
Demonstrates CadQuery integration with Marimo. Excellent as a secondary backend option.

**Features:**
- Parametric bearing block
- Fluent API demonstration
- Powerful selector system
- Assembly example
- Export functionality

**To run:**
```bash
pip install cadquery marimo
marimo edit cadquery_poc.py
```

### 4. `ocp_poc.py` (Educational Only)
Demonstrates direct OCP (OpenCascade) usage. **NOT recommended** for user-facing API.

**Purpose:**
- Shows why high-level wrappers are needed
- Educational comparison
- Understanding the underlying technology

**To run:**
```bash
pip install cadquery marimo  # OCP comes with cadquery
marimo edit ocp_poc.py
```

## Installation

### Minimal Installation (Build123d only)
```bash
pip install build123d marimo
```

### Full Installation (All libraries)
```bash
pip install build123d cadquery marimo ocp-vscode
```

### Optional Visualization
```bash
# For Build123d visualization
pip install ocp-vscode

# For CadQuery visualization
pip install jupyter-cadquery
```

## Running the Examples

### In Marimo
```bash
# Start any example
marimo edit examples/build123d_poc.py

# Or run in browser
marimo run examples/build123d_poc.py
```

### As Python Scripts
```bash
python examples/build123d_poc.py
```

## Testing

All examples are automatically tested via GitHub Actions CI to ensure:
- Valid Python syntax
- Successful imports
- Proper Marimo app structure
- Basic geometry creation works

Run tests locally:
```bash
python tests/test_examples.py
```

See [../tests/README.md](../tests/README.md) for more details.

## Key Findings

### Build123d Advantages
✅ Native Marimo/notebook integration
✅ Modern Python API (context managers, type hints)
✅ Multiple modeling paradigms
✅ Powerful selector system
✅ Active development

### CadQuery Advantages
✅ Mature and stable
✅ Excellent documentation
✅ Large community
✅ Fluent, chainable API
✅ Rich ecosystem

### OCP Considerations
⚠️ Too low-level for users
⚠️ Verbose and complex
⚠️ Not Pythonic
✅ Maximum control
✅ Foundation for other libraries

## Recommendation

**Primary Backend:** Build123d
**Secondary Backend:** CadQuery (optional)
**Direct OCP:** Only for advanced internal use

## Next Steps

1. Implement marimocad wrapper around Build123d
2. Create component library (screws, gears, bearings, etc.)
3. Add Marimo-specific UI components
4. Implement visualization integration
5. Consider adding CadQuery support as alternative

## References

- [Build123d Documentation](https://build123d.readthedocs.io/)
- [CadQuery Documentation](https://cadquery.readthedocs.io/)
- [OCP Repository](https://github.com/CadQuery/OCP)
- [Marimo Documentation](https://docs.marimo.io/)
- [CAD Library Comparison](../CAD_LIBRARY_COMPARISON.md)
