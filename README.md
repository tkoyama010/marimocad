# marimocad

CAD file import/export functionality for marimo notebooks.

## Features

- 📁 **Multiple Format Support**: STEP, STL, and OBJ file formats
- 📥 **Import/Export**: Bidirectional file conversion
- 🔍 **Format Detection**: Automatic format detection from file content
- ✅ **Validation**: File format validation
- 📊 **Progress Tracking**: Progress callbacks for large files
- 🧪 **Well Tested**: Comprehensive test suite

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

### Import a CAD file

```python
from marimocad import import_file

# Import any supported format (auto-detected)
model = import_file("model.stl")

print(f"Format: {model['format']}")
print(f"Vertices: {len(model['vertices'])}")
print(f"Faces: {len(model['faces'])}")
```

### Export a CAD file

```python
from marimocad import export_file

data = {
    'vertices': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 1.0, 0.0)],
    'faces': [(0, 1, 2)],
}

# Format auto-detected from extension
export_file("model.stl", data)
```

### Track Progress

```python
from marimocad import import_file

def progress(percent):
    print(f"Loading: {percent}%")

model = import_file("large_model.stl", progress_callback=progress)
```

## Supported Formats

| Format | Import | Export | Description |
|--------|--------|--------|-------------|
| STEP   | ✅     | ✅     | ISO 10303 standard format |
| STL    | ✅     | ✅     | Stereolithography (ASCII & binary) |
| OBJ    | ✅     | ✅     | Wavefront object format |

For detailed format specifications and usage examples, see [FORMATS.md](FORMATS.md).

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=marimocad --cov-report=html
```

### Project Structure

```
marimocad/
├── marimocad/          # Main package
│   ├── __init__.py     # Package exports
│   └── io.py           # Core I/O functionality
├── tests/              # Test suite
│   ├── test_io.py      # I/O tests
│   └── fixtures.py     # Test fixtures
├── FORMATS.md          # Format documentation
├── pyproject.toml      # Package configuration
└── README.md           # This file
```

## Documentation

- [Format Specifications](FORMATS.md) - Detailed documentation for each supported format
- API documentation available in docstrings

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure tests pass before submitting PRs.

## Related Projects

- [marimo](https://github.com/marimo-team/marimo) - Reactive Python notebooks
- [pythonocc-core](https://github.com/tpaviot/pythonocc-core) - Python bindings for OpenCASCADE