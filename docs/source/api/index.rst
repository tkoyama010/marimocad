API Reference
=============

This section contains the complete API reference for marimocad.

.. toctree::
   :maxdepth: 2

   shapes
   operations
   transforms

Core Modules
------------

marimocad provides a simple, composable API organized into three main modules:

shapes
~~~~~~
Basic 3D geometric shapes that serve as building blocks.

operations
~~~~~~~~~~
Boolean operations for combining shapes using constructive solid geometry.

transforms
~~~~~~~~~~
Functions for transforming shapes in 3D space.

Quick Reference
---------------

Shapes
~~~~~~

.. autosummary::
   :toctree: generated

   marimocad.Box
   marimocad.Cylinder
   marimocad.Sphere

Operations
~~~~~~~~~~

.. autosummary::
   :toctree: generated

   marimocad.union
   marimocad.intersection
   marimocad.difference

Transforms
~~~~~~~~~~

.. autosummary::
   :toctree: generated

   marimocad.translate
   marimocad.rotate
   marimocad.scale
