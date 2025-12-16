"""marimocad - CAD tools for marimo notebooks.

This package provides CAD functionality for creating and manipulating
3D geometries in marimo notebooks with seamless integration with Marimo's
reactive programming model.

Architecture:
    - Public API: Pythonic functions for CAD operations
    - Core Layer: Backend-agnostic abstractions
    - Backend Layer: Build123d primary, CadQuery secondary
    - Marimo Integration: Reactive viewer and UI components

For detailed documentation, see:
    - API_SPECIFICATION.md: Complete API reference
    - ARCHITECTURE.md: System architecture and design
    - DESIGN_DECISIONS.md: Key design rationale
    - EXAMPLES.md: Usage examples

Example:
    >>> import marimocad as mc
    >>> box = mc.box(10, 10, 10)
    >>> mc.viewer(box)
"""

__version__ = "0.1.dev0"

# Import viewer components for public API
from marimocad.marimo import GeometryCard, parametric_model, viewer


__all__ = ["GeometryCard", "__version__", "parametric_model", "viewer"]
