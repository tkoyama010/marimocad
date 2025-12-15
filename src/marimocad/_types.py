"""Type definitions for marimocad geometry.

This module defines the core type system for marimocad, providing
backend-agnostic abstractions for CAD geometry.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Geometry(Protocol):
    """Base protocol for all geometry objects."""

    def __repr__(self) -> str:
        """Return string representation."""
        ...


@runtime_checkable
class Vertex(Geometry, Protocol):
    """Protocol for vertex geometry."""


@runtime_checkable
class Edge(Geometry, Protocol):
    """Protocol for edge geometry."""


@runtime_checkable
class Wire(Geometry, Protocol):
    """Protocol for wire geometry."""


@runtime_checkable
class Face(Geometry, Protocol):
    """Protocol for face/2D surface geometry."""


@runtime_checkable
class Solid(Geometry, Protocol):
    """Protocol for solid/3D geometry."""


__all__ = [
    "Edge",
    "Face",
    "Geometry",
    "Solid",
    "Vertex",
    "Wire",
]
