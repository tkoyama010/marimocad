# marimocad

CAD tools for marimo notebooks - Interactive 3D modeling and computational geometry.

## Installation

```bash
pip install marimocad
```

## Development

For development, clone the repository and install with development dependencies:

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

MIT License - see LICENSE file for details.
