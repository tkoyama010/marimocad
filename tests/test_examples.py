#!/usr/bin/env python3
"""Test script to verify that example code is working.

This script tests:
1. Python syntax validation
2. Import validation
3. Basic geometry creation
4. Marimo app structure
"""

import ast

from pathlib import Path

import pytest


def test_syntax(filepath):
    """Test that file has valid Python syntax."""
    print(f"\nTesting syntax: {filepath}")
    content = Path(filepath).read_text(encoding="utf-8")
    # This will raise SyntaxError if invalid, causing test to fail
    ast.parse(content)
    print("  ✓ Valid Python syntax")


def test_imports(filepath):
    """Test that imports work correctly."""
    print(f"\nTesting imports: {filepath}")
    # For now, just check that the file can be parsed
    # Full import testing would require the actual libraries
    content = Path(filepath).read_text(encoding="utf-8")
    tree = ast.parse(content)
    # Verify it has import statements
    has_imports = any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
    assert has_imports, f"File {filepath} has no import statements"
    print("  ✓ File has import statements")


def test_marimo_structure(filepath):
    """Test that file is a valid marimo app."""
    print(f"\nTesting marimo structure: {filepath}")
    content = Path(filepath).read_text(encoding="utf-8")

    assert "marimo.App" in content, f"File {filepath} is missing marimo.App definition"
    assert "@app.cell" in content, f"File {filepath} is missing @app.cell decorator"

    print("  ✓ Valid marimo app structure")


def test_geometry_creation():
    """Test basic geometry creation with each library."""
    print("\nTesting basic geometry creation:")

    # Test Build123d
    try:
        from build123d import Box, BuildPart

        with BuildPart() as test:
            Box(10, 10, 10)
        print("  ✓ Build123d: Basic geometry creation works")
    except ImportError:
        print("  ⚠ Build123d not installed, skipping")
    except Exception as e:
        pytest.fail(f"Build123d error: {e}")

    # Test CadQuery
    try:
        import cadquery as cq

        box = cq.Workplane("XY").box(10, 10, 10)
        print("  ✓ CadQuery: Basic geometry creation works")
    except ImportError:
        print("  ⚠ CadQuery not installed, skipping")
    except Exception as e:
        pytest.fail(f"CadQuery error: {e}")

    # Test OCP
    try:
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox

        box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
        print("  ✓ OCP: Basic geometry creation works")
    except ImportError:
        print("  ⚠ OCP not installed, skipping")
    except Exception as e:
        pytest.fail(f"OCP error: {e}")
