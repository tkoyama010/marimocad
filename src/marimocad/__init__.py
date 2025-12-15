"""
marimocad: Interactive CAD modeling with marimo notebooks.

This package provides tools for creating and manipulating CAD models
in an interactive marimo notebook environment.
"""

__version__ = "0.1.0"

from .shapes import Box, Cylinder, Sphere
from .operations import union, intersection, difference
from .transforms import translate, rotate, scale

__all__ = [
    "Box",
    "Cylinder",
    "Sphere",
    "union",
    "intersection",
    "difference",
    "translate",
    "rotate",
    "scale",
]
