# marimocad

[![CI](https://github.com/tkoyama010/marimocad/actions/workflows/ci.yml/badge.svg)](https://github.com/tkoyama010/marimocad/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/marimocad.svg)](https://badge.fury.io/py/marimocad)
[![Python versions](https://img.shields.io/pypi/pyversions/marimocad.svg)](https://pypi.org/project/marimocad/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CAD tools for marimo notebooks.

## Installation

### From PyPI (recommended)

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

For development, install with optional dependencies:

```bash
pip install -e ".[dev]"
```

## Requirements

- Python 3.9 or higher
- marimo

## Usage

```python
import marimocad

# Check version
print(marimocad.__version__)
```

## Development

### Running tests

```bash
pytest tests/
```

### Linting

```bash
ruff check .
```

### Type checking

```bash
mypy src/marimocad
```

### Building the package

```bash
python -m build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Tetsuo Koyama (@tkoyama010)

## Links

- [GitHub Repository](https://github.com/tkoyama010/marimocad)
- [Issue Tracker](https://github.com/tkoyama010/marimocad/issues)
- [PyPI Package](https://pypi.org/project/marimocad/)