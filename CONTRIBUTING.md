# Contributing to marimocad

Thank you for your interest in contributing to marimocad! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

**Our Standards:**
- Be welcoming and inclusive
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of CAD concepts
- Familiarity with marimo notebooks (recommended)

### Find an Issue

1. Check the [issue tracker](https://github.com/tkoyama010/marimocad/issues)
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to let others know you're working on it

## Development Setup

1. **Fork the repository**

   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/marimocad.git
   cd marimocad
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/tkoyama010/marimocad.git
   ```

4. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install in development mode**

   ```bash
   pip install -e ".[dev,docs]"
   ```

6. **Verify installation**

   ```bash
   python -c "import marimocad; print(marimocad.__version__)"
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check if the bug has already been reported
- Collect information about the bug (Python version, OS, error messages)

**Bug Report Template:**
```markdown
## Description
A clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- marimocad version: [e.g., 0.1.0]

## Additional Context
Any other relevant information
```

### Suggesting Features

Feature requests are welcome! Please provide:
- Clear description of the feature
- Use cases and examples
- Why this feature would be useful
- Possible implementation approach (optional)

### Contributing Code

1. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, readable code
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

   Follow conventional commit format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `style:` for formatting changes
   - `chore:` for maintenance tasks

4. **Keep your fork updated**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill in the PR template
   - Link related issues

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Use absolute imports, group standard library, third-party, and local
- **Type hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings

### Code Formatting

We use automated tools to maintain code quality:

```bash
# Format code with Black
black src tests

# Check with Ruff
ruff check src tests

# Type check with mypy
mypy src
```

### Example Code Style

```python
"""Module docstring explaining the purpose."""

from typing import Optional, Tuple
import numpy as np


class Shape:
    """Brief description of the class.
    
    Longer description if needed, explaining key concepts.
    
    Attributes:
        position: The (x, y, z) position of the shape.
        name: Optional name for the shape.
    
    Examples:
        >>> shape = Shape(name="example")
        >>> shape.position
        array([0., 0., 0.])
    """
    
    def __init__(self, name: str = "") -> None:
        """Initialize a shape.
        
        Args:
            name: Optional name for the shape.
        """
        self.position = np.array([0.0, 0.0, 0.0])
        self.name = name
    
    def calculate_volume(self) -> float:
        """Calculate the volume of the shape.
        
        Returns:
            The volume in cubic units.
        
        Raises:
            NotImplementedError: If method not implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement this method")
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=marimocad --cov-report=html

# Run specific test file
pytest tests/test_shapes.py

# Run specific test
pytest tests/test_shapes.py::test_box_volume
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Include docstrings for complex tests

**Example Test:**

```python
def test_box_volume():
    """Test that box volume calculation is correct."""
    box = Box(width=2, height=3, depth=4)
    assert box.volume() == 24.0


def test_box_invalid_dimensions():
    """Test that negative dimensions raise ValueError."""
    with pytest.raises(ValueError):
        Box(width=-1, height=5, depth=5)
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Test public APIs thoroughly
- Don't test private methods directly

## Documentation

### Docstring Requirements

All public modules, classes, functions, and methods must have docstrings:

```python
def translate(shape: Shape, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Shape:
    """Translate (move) a shape by the specified distances.
    
    Args:
        shape: The shape to translate.
        x: Distance to move along the x-axis.
        y: Distance to move along the y-axis.
        z: Distance to move along the z-axis.
    
    Returns:
        The translated shape (same object, modified in place).
    
    Examples:
        Move a box to a new position::
        
            box = Box(width=10, height=5, depth=3)
            translate(box, x=10, y=5, z=2)
    """
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build HTML documentation
cd docs
make html

# View documentation
# Open docs/_build/html/index.html in your browser
```

### Documentation Structure

- **README.md**: Quick start and overview
- **docs/**: Full documentation
  - `architecture.md`: System architecture
  - `api/`: API reference (auto-generated)
  - `tutorials/`: Step-by-step guides
  - `examples/`: Example gallery
- **examples/**: Runnable example notebooks

## Pull Request Process

1. **Ensure your PR is ready**
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] Documentation updated
   - [ ] Changelog updated (if applicable)

2. **Create a clear PR description**
   - Describe what changes you made
   - Explain why you made them
   - Link to related issues
   - Include screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Related Issues
   Fixes #123
   
   ## Changes Made
   - Change 1
   - Change 2
   
   ## Testing
   How you tested your changes
   
   ## Checklist
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Code follows style guide
   ```

4. **Review Process**
   - Maintainers will review your PR
   - Address review comments
   - Make requested changes
   - Once approved, your PR will be merged

5. **After Merge**
   - Your contribution will be acknowledged
   - You'll be added to contributors list
   - Delete your feature branch

## Questions?

If you have questions:
- Check existing documentation
- Search closed issues
- Ask in a new issue
- Contact maintainers

## Thank You!

Your contributions make marimocad better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚀**
