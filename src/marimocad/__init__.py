"""
marimocad - A modern CAD library for Python with marimo integration.

This package provides core CAD functionality for creating and manipulating 3D geometries.
"""

from marimocad.primitives import box, sphere, cylinder, cone, torus
from marimocad.transforms import translate, rotate, scale
from marimocad.boolean import union, difference, intersection
from marimocad.sketch import Sketch
from marimocad.operations import extrude, revolve, sweep

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
