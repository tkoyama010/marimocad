# Tests

This directory contains tests for the marimocad project.

## test_examples.py

Tests that verify the example code is working correctly.

### What it tests:
1. **Python syntax validation** - Ensures all example files have valid Python syntax
2. **Import validation** - Verifies all required imports work
3. **Marimo structure** - Checks that files are properly structured Marimo apps
4. **Geometry creation** - Tests basic geometry creation with each library

### Requirements:
```bash
pip install marimo build123d cadquery
```

### Running tests locally:
```bash
python tests/test_examples.py
```

### CI Integration:
Tests are automatically run via GitHub Actions on:
- Push to main or copilot/** branches (when examples/ directory changes)
- Pull requests to main (when examples/ directory changes)

See `.github/workflows/test-examples.yml` for CI configuration.

## Test Coverage

Currently tested:
- ✅ Python syntax validation for all examples
- ✅ Import validation for build123d, cadquery, and OCP
- ✅ Marimo app structure validation
- ✅ Basic geometry creation with each library

Future tests could include:
- More complex geometry operations
- Export functionality
- Performance benchmarks
- Integration tests with actual Marimo runtime
