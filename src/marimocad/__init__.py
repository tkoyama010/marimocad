"""
marimocad - A modern CAD library for Python with marimo integration.

This package provides core CAD functionality for creating and manipulating 3D geometries.
"""

from marimocad.boolean import difference, intersection, union
from marimocad.operations import extrude, revolve, sweep
from marimocad.primitives import box, cone, cylinder, sphere, torus
from marimocad.sketch import Sketch
from marimocad.transforms import rotate, scale, translate

__version__ = "0.1.0"

__all__ = [
    # Primitives
    "box",
    "sphere",
    "cylinder",
    "cone",
    "torus",
    # Transforms
    "translate",
    "rotate",
    "scale",
    # Boolean operations
    "union",
    "difference",
    "intersection",
    # Sketch
    "Sketch",
    # Operations
    "extrude",
    "revolve",
    "sweep",
]
