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
    >>> sphere = mc.sphere(5)
    >>> result = mc.union(box, sphere)
"""

from marimocad._types import Edge, Face, Geometry, Solid, Vertex, Wire
from marimocad.extrude import extrude, loft, revolve, sweep
from marimocad.geometry import (
    box,
    circle,
    cone,
    cylinder,
    polygon,
    rectangle,
    sphere,
    torus,
)
from marimocad.operations import (
    intersect,
    mirror,
    rotate,
    scale,
    subtract,
    translate,
    union,
)


__version__ = "0.1.dev0"

__all__ = [
    "Edge",
    "Face",
    "Geometry",
    "Solid",
    "Vertex",
    "Wire",
    "__version__",
    "box",
    "circle",
    "cone",
    "cylinder",
    "extrude",
    "intersect",
    "loft",
    "mirror",
    "polygon",
    "rectangle",
    "revolve",
    "rotate",
    "scale",
    "sphere",
    "subtract",
    "sweep",
    "torus",
    "translate",
    "union",
]
