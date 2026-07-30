# Contributing to marimocad

Thank you for your interest in contributing to marimocad! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/tkoyama010/marimocad.git
   cd marimocad
   ```

2. Install dependencies using uv (recommended):
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Sync dependencies
   uv sync
   ```

   Or using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Quality and Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting Python code. Ruff is configured with comprehensive rule sets to ensure code quality, consistency, and best practices.

### Running Ruff

To check your code with Ruff:

```bash
# Check all files for linting issues
ruff check .

# Check all files and automatically fix issues where possible
ruff check --fix .

# Format code with Ruff
ruff format .
```

### Pre-commit Hooks

Pre-commit hooks are configured to automatically run Ruff and other checks before each commit. This ensures that all committed code meets the project's quality standards.

The pre-commit hooks will:
- Run Ruff linting with automatic fixes
- Format code with Ruff
- Check for trailing whitespace
- Check YAML, TOML, and JSON syntax
- Detect large files, merge conflicts, and private keys
- Run mypy for type checking

To manually run pre-commit on all files:

```bash
pre-commit run --all-files
```

### Ruff Configuration

The project uses a comprehensive set of Ruff rules covering:
- **Code Style**: PEP 8 compliance (E, W)
- **Error Prevention**: PyFlakes (F), flake8-bugbear (B)
- **Best Practices**: flake8-simplify (SIM), Pylint (PL)
- **Type Hints**: flake8-annotations (ANN)
- **Documentation**: pydocstyle (D) with Google convention
- **Security**: flake8-bandit (S)
- **Modern Python**: pyupgrade (UP), flynt (FLY)
- **Performance**: Perflint (PERF)
- And many more!

See `pyproject.toml` for the complete configuration.

### Type Checking

Run mypy to check type annotations:

```bash
mypy src/marimocad
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=marimocad --cov-report=term-missing
```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the code style guidelines.

3. Write tests for your changes.

4. Ensure all tests pass and linting checks succeed:
   ```bash
   pytest
   ruff check .
   mypy src/marimocad
   ```

5. Commit your changes (pre-commit hooks will run automatically):
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. Push your branch and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use Google-style docstrings for all public APIs
- Add type hints to all function signatures
- Write clear, descriptive commit messages
- Keep functions focused and modular
- Add tests for new functionality
- Update documentation as needed

## Documentation

- Use Google-style docstrings
- Include examples in docstrings where appropriate
- Keep the README.md up to date
- Document any new dependencies or setup requirements

## Release Process

Releases are managed through GitHub Actions workflows. Only maintainers can create releases.

### Creating a Release

1. **Prepare the release:**
   - Ensure all tests pass on the main branch
   - Update documentation if needed
   - Review and merge all PRs intended for the release

2. **Trigger the release workflow:**
   - Go to Actions → Release workflow
   - Click "Run workflow"
   - Enter the version number (e.g., `0.1.0`, `1.0.0`)
   - The workflow will:
     - Update the version in `src/marimocad/__init__.py`
     - Create a git tag
     - Generate release notes
     - Create a GitHub Release

3. **Publish to PyPI:**
   - The GitHub Release will automatically trigger the PyPI publish workflow
   - The package will be built and published to PyPI using trusted publishing

### Testing Releases

Before publishing to PyPI, you can test the release on TestPyPI:

1. Go to Actions → Publish to PyPI workflow
2. Click "Run workflow"
3. Select "testpypi" as the target
4. The package will be published to https://test.pypi.org/project/marimocad/

Test the installation:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ marimocad
```

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, backwards compatible

## Questions?

If you have any questions or need help, please open an issue on GitHub.

## License

By contributing to marimocad, you agree that your contributions will be licensed under the MIT License.
