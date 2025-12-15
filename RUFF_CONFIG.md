# Ruff Configuration Summary

This document provides an overview of the Ruff linting configuration for the marimocad project.

## Overview

The project uses [Ruff](https://docs.astral.sh/ruff/) with a comprehensive set of rules enabled to ensure high code quality, consistency, and adherence to Python best practices.

## Configuration Details

### Basic Settings
- **Line Length**: 100 characters
- **Target Python Version**: 3.9+
- **Docstring Convention**: Google style

### Enabled Rule Sets

The configuration enables the following rule categories (see [pyproject.toml](pyproject.toml) for complete details):

| Code | Category | Description |
|------|----------|-------------|
| A | flake8-builtins | Checks for shadowing of built-in names |
| ANN | flake8-annotations | Enforces type annotations |
| ARG | flake8-unused-arguments | Detects unused function arguments |
| B | flake8-bugbear | Finds likely bugs and design problems |
| BLE | flake8-blind-except | Prevents blind exception catching |
| C4 | flake8-comprehensions | Suggests better list/dict/set comprehensions |
| C90 | mccabe | Checks code complexity |
| COM | flake8-commas | Enforces trailing comma style |
| D | pydocstyle | Enforces docstring conventions (Google style) |
| DTZ | flake8-datetimez | Prevents naive datetime usage |
| E | pycodestyle errors | Checks for PEP 8 errors |
| EM | flake8-errmsg | Enforces good exception message practices |
| ERA | eradicate | Finds commented-out code |
| EXE | flake8-executable | Checks shebang presence and format |
| F | pyflakes | Detects various Python errors |
| FA | flake8-future-annotations | Enforces future annotations |
| FBT | flake8-boolean-trap | Prevents boolean trap anti-pattern |
| FIX | flake8-fixme | Detects FIXME, TODO, and other comments |
| FLY | flynt | Suggests f-string usage |
| FURB | refurb | Suggests code modernization |
| G | flake8-logging-format | Enforces logging best practices |
| I | isort | Sorts and organizes imports |
| ICN | flake8-import-conventions | Enforces import naming conventions |
| INP | flake8-no-pep420 | Enforces `__init__.py` presence |
| INT | flake8-gettext | Checks gettext usage |
| ISC | flake8-implicit-str-concat | Prevents implicit string concatenation |
| LOG | flake8-logging | Enforces logging best practices |
| N | pep8-naming | Enforces PEP 8 naming conventions |
| NPY | NumPy-specific rules | NumPy-specific best practices |
| PERF | Perflint | Suggests performance improvements |
| PGH | pygrep-hooks | Various code quality checks |
| PIE | flake8-pie | Miscellaneous linting rules |
| PL | Pylint | Comprehensive code quality checks |
| PT | flake8-pytest-style | Enforces pytest best practices |
| PTH | flake8-use-pathlib | Suggests pathlib over os.path |
| PYI | flake8-pyi | Stub file checks |
| Q | flake8-quotes | Enforces quote style |
| RET | flake8-return | Checks return statement patterns |
| RSE | flake8-raise | Enforces raise statement best practices |
| RUF | Ruff-specific rules | Ruff's own rules |
| S | flake8-bandit | Security checks |
| SIM | flake8-simplify | Suggests code simplification |
| SLF | flake8-self | Prevents private member access |
| SLOT | flake8-slots | Enforces `__slots__` usage |
| T10 | flake8-debugger | Detects debugger statements |
| T20 | flake8-print | Detects print statements |
| TCH | flake8-type-checking | Type checking imports optimization |
| TD | flake8-todos | Enforces TODO format |
| TID | flake8-tidy-imports | Enforces import organization |
| TRY | tryceratops | Exception handling best practices |
| UP | pyupgrade | Suggests modern Python syntax |
| W | pycodestyle warnings | Checks for PEP 8 warnings |
| YTT | flake8-2020 | Prevents sys.version usage patterns |

### Ignored Rules

A minimal set of rules are ignored to avoid conflicts:

- **ANN401**: Dynamically typed expressions (Any) are disallowed
- **COM812**: Trailing comma missing (conflicts with formatter)
- **D203**: 1 blank line required before class docstring (conflicts with D211)
- **D213**: Multi-line docstring summary should start at the second line (conflicts with D212)
- **ISC001**: Implicitly concatenated string literals (conflicts with formatter)

### Per-File Ignores

Different rules apply to different file types:

**`__init__.py` files:**
- D104: Missing docstring in public package
- F401: Imported but unused

**Test files (`tests/**/*.py`):**
- Various docstring and annotation requirements relaxed
- S101: Use of assert detected (needed for pytest)
- PLR2004: Magic value used in comparison

**Example files (`examples/**/*.py`):**
- D100: Missing docstring in public module
- INP001: File is part of an implicit namespace package
- T201: print found (useful in examples)

## Complexity Limits

- **Maximum cyclomatic complexity**: 10
- **Maximum arguments**: 5
- **Maximum branches**: 12
- **Maximum returns**: 6
- **Maximum statements**: 50

## Running Ruff

### Check for issues:
```bash
ruff check .
```

### Automatically fix issues:
```bash
ruff check --fix .
```

### Format code:
```bash
ruff format .
```

### Check formatting:
```bash
ruff format --check .
```

## Pre-commit Integration

Ruff runs automatically via pre-commit hooks before each commit. Install with:

```bash
pre-commit install
```

Run manually on all files:

```bash
pre-commit run --all-files
```

## CI/CD Integration

Ruff checks run automatically in GitHub Actions on all pull requests and pushes to main. See [.github/workflows/lint.yml](.github/workflows/lint.yml) for details.

## Expected Code Quality Impact

With this configuration, the following aspects are enforced:

1. **Type Safety**: All functions must have type annotations
2. **Documentation**: All public APIs must have Google-style docstrings
3. **Security**: Common security issues are detected (SQL injection, hardcoded passwords, etc.)
4. **Performance**: Inefficient patterns are flagged
5. **Modernization**: Code uses modern Python syntax (f-strings, pathlib, etc.)
6. **Consistency**: Import order, naming conventions, and code style are standardized
7. **Maintainability**: Code complexity is limited, unused code is detected

## Learning More

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
