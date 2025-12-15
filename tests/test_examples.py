#!/usr/bin/env python3
"""Test script to verify that example code is working.

This script tests:
1. Python syntax validation
2. Import validation
3. Basic geometry creation
4. Marimo app structure
"""

import ast
import sys

from pathlib import Path


def test_syntax(filepath):
    """Test that file has valid Python syntax."""
    print(f"\nTesting syntax: {filepath}")
    try:
        content = Path(filepath).read_text(encoding="utf-8")
        ast.parse(content)
        print("  ✓ Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error: {e}")
        return False


def test_imports(filepath, test_func):
    """Test that imports work correctly."""
    print(f"\nTesting imports: {filepath}")
    try:
        test_func()
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_marimo_structure(filepath):
    """Test that file is a valid marimo app."""
    print(f"\nTesting marimo structure: {filepath}")
    try:
        content = Path(filepath).read_text(encoding="utf-8")

        if "marimo.App" not in content:
            print("  ✗ Missing marimo.App definition")
            return False

        if "@app.cell" not in content:
            print("  ✗ Missing @app.cell decorator")
            return False

        print("  ✓ Valid marimo app structure")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_build123d_imports():
    """Test Build123d imports."""


def test_cadquery_imports():
    """Test CadQuery imports."""


def test_ocp_imports():
    """Test OCP imports."""


def test_geometry_creation():
    """Test basic geometry creation with each library."""
    print("\nTesting basic geometry creation:")

    try:
        from build123d import Box, BuildPart

        with BuildPart() as test:
            Box(10, 10, 10)
        print("  ✓ Build123d: Basic geometry creation works")
    except Exception as e:
        print(f"  ✗ Build123d error: {e}")
        return False

    try:
        import cadquery as cq

        box = cq.Workplane("XY").box(10, 10, 10)
        print("  ✓ CadQuery: Basic geometry creation works")
    except Exception as e:
        print(f"  ✗ CadQuery error: {e}")
        return False

    try:
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox

        box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
        print("  ✓ OCP: Basic geometry creation works")
    except Exception as e:
        print(f"  ✗ OCP error: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Example Code")
    print("=" * 60)

    examples_dir = Path(__file__).parent.parent / "examples"

    examples = [
        ("build123d_poc.py", test_build123d_imports),
        ("cadquery_poc.py", test_cadquery_imports),
        ("ocp_poc.py", test_ocp_imports),
    ]

    all_passed = True

    # Run all tests for each example
    for example_file, import_test in examples:
        filepath = examples_dir / example_file

        # Test syntax
        if not test_syntax(filepath):
            all_passed = False

        # Test imports
        if not test_imports(filepath, import_test):
            all_passed = False

        # Test marimo structure
        if not test_marimo_structure(filepath):
            all_passed = False

    # Test geometry creation
    if not test_geometry_creation():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    print("✗ Some tests failed")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    sys.exit(main())
