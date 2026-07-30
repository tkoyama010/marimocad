# marimocad Architecture

## Overview

This document describes the architecture of marimocad, a CAD library designed for interactive parametric modeling in Marimo notebooks. The architecture emphasizes modularity, extensibility, and seamless integration with Marimo's reactive programming model.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Marimo Notebook                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     User Interface Layer                          │  │
│  │  • Interactive controls (sliders, inputs, buttons)               │  │
│  │  • Reactive cells with @app.cell decorators                       │  │
│  │  • Parameter binding and state management                         │  │
│  └────────────────────────────┬─────────────────────────────────────┘  │
└─────────────────────────────────┼─────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       marimocad Public API                               │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  marimocad.geometry      │  marimocad.operations                  │  │
│  │  • box(), sphere(), etc. │  • translate(), rotate()               │  │
│  │  • circle(), polygon()   │  • union(), subtract()                 │  │
│  │                          │  • fillet(), chamfer()                 │  │
│  ├──────────────────────────┼────────────────────────────────────────┤  │
│  │  marimocad.components    │  marimocad.assembly                    │  │
│  │  • screw(), gear()       │  • Assembly class                      │  │
│  │  • bearing(), i_beam()   │  • Constraints                         │  │
│  ├──────────────────────────┼────────────────────────────────────────┤  │
│  │  marimocad.io            │  marimocad.marimo                      │  │
│  │  • export_step(), etc.   │  • viewer()                            │  │
│  │  • import_step(), etc.   │  • parametric_model()                  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Core Abstraction Layer                            │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  • Backend-agnostic interfaces (Protocols)                        │  │
│  │  • Type system (Solid, Face, Edge, Vertex, Wire)                  │  │
│  │  • Error handling and validation                                  │  │
│  │  • Geometry wrapping and conversion                               │  │
│  │  • Reactive state management                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Backend Adapter Layer                            │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Build123dBackend (Primary)     │  CadQueryBackend (Secondary)    │  │
│  │  • Translates API to Build123d  │  • Translates API to CadQuery   │  │
│  │  • Build123d-specific features  │  • CadQuery-specific features   │  │
│  │  • Performance optimizations    │  • Compatibility layer          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAD Backend Libraries                             │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │      Build123d          │  │         CadQuery                     │  │
│  │  • Primary backend      │  │  • Alternative backend               │  │
│  │  • Native notebook      │  │  • Mature and stable                 │  │
│  │  • Multiple paradigms   │  │  • Large community                   │  │
│  └────────────┬────────────┘  └──────────────┬──────────────────────┘  │
│               └────────────────────┬──────────┘                          │
│                                    ▼                                     │
│               ┌──────────────────────────────────────┐                   │
│               │      OpenCascade (OCP)               │                   │
│               │  • Core geometric kernel             │                   │
│               │  • BREP representation               │                   │
│               │  • Boolean operations                │                   │
│               └──────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Visualization & Export                             │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  • Build123d native 3D viewer (via ocp-tessellate)               │  │
│  │  • STEP, STL, SVG exporters                                       │  │
│  │  • Mesh generation                                                │  │
│  │  • HTML/Canvas rendering for notebooks                            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. Marimo Notebook (User Interface Layer)

**Purpose**: Provide interactive interface for users to create parametric models

**Components**:
- **Reactive Cells**: Marimo cells that automatically re-execute when dependencies change
- **UI Controls**: Sliders, inputs, dropdowns for parameter control
- **State Management**: Marimo's reactive state system

**Key Features**:
- Automatic dependency tracking
- Incremental computation
- Interactive parameter adjustment
- Real-time model updates

### 2. Public API Layer

**Purpose**: Provide a clean, Pythonic interface for CAD operations

**Modules**:

#### `marimocad.geometry`
- Primitive creation (box, sphere, cylinder, etc.)
- 2D shape creation (circle, rectangle, polygon)
- Geometry composition

#### `marimocad.operations`
- Transformations (translate, rotate, scale, mirror)
- Boolean operations (union, subtract, intersect)
- Modifications (fillet, chamfer, shell, offset)
- Extrusion and revolution

#### `marimocad.components`
- Pre-built mechanical components (screws, gears, bearings)
- Standard profiles (I-beam, channel, etc.)
- Parametric component library

#### `marimocad.assembly`
- Multi-part assembly management
- Constraint system
- Assembly solver

#### `marimocad.io`
- Export functions (STEP, STL, SVG, etc.)
- Import functions
- File format conversion

#### `marimocad.marimo`
- Viewer component for 3D visualization
- Parametric model wrapper
- Geometry info cards
- Marimo-specific utilities

**Design Principles**:
- Functions over classes for simplicity
- Type hints for all public APIs
- Consistent naming conventions
- Clear, descriptive docstrings

### 3. Core Abstraction Layer

**Purpose**: Provide backend-agnostic interfaces and common functionality

**Components**:

#### Type System
```python
# Protocol-based type system
class Geometry(Protocol):
    """Base geometry interface."""

class Solid(Geometry):
    """3D solid geometry."""

class Face(Geometry):
    """2D surface geometry."""

class Edge(Geometry):
    """1D curve geometry."""

class Vertex(Geometry):
    """0D point geometry."""
```

#### Geometry Wrapper
- Wraps backend-specific geometry objects
- Provides uniform interface across backends
- Handles type conversions
- Manages geometry metadata

#### Reactive State Manager
- Caches computed geometries
- Tracks dependencies
- Invalidates cache on parameter changes
- Optimizes recomputation

#### Error Handling
- Custom exception hierarchy
- Descriptive error messages
- Validation before backend calls
- Graceful degradation

### 4. Backend Adapter Layer

**Purpose**: Translate abstract API calls to backend-specific operations

#### Build123d Backend (Primary)
```python
class Build123dBackend:
    """Primary backend using Build123d."""

    def create_box(self, length, width, height, center):
        """Create box using Build123d."""
        from build123d import Box, BuildPart
        with BuildPart() as part:
            Box(length, width, height)
        return self._wrap(part.part)

    def union(self, *geoms):
        """Union operation using Build123d."""
        # Implementation
```

**Features**:
- Native notebook support via `_repr_html_()`
- Context manager API
- Advanced selectors
- Multiple modeling paradigms

#### CadQuery Backend (Secondary)
```python
class CadQueryBackend:
    """Alternative backend using CadQuery."""

    def create_box(self, length, width, height, center):
        """Create box using CadQuery."""
        import cadquery as cq
        workplane = cq.Workplane("XY")
        box = workplane.box(length, width, height, centered=center)
        return self._wrap(box)
```

**Features**:
- Fluent API
- Workplane-based modeling
- Mature and stable
- Large community

### 5. CAD Backend Libraries

#### Build123d
- Modern Python API
- Multiple modeling modes (Builder, Algebra, Direct)
- Built-in notebook integration
- Active development

#### CadQuery
- Fluent, chainable API
- Workplane-centric
- Excellent documentation
- Large user base

#### OpenCascade (OCP)
- Core geometric kernel
- BREP (Boundary Representation)
- Boolean algorithms
- Mesh generation

### 6. Visualization & Export

#### Visualization
- **Build123d native rendering**: Interactive 3D viewer using ocp-tessellate (included with Build123d)
- **Three.js**: Alternative web-based rendering for WASM deployment
- **SVG**: 2D projections for documentation

#### Export
- **STEP**: Industry-standard CAD format
- **STL**: 3D printing and mesh applications
- **SVG**: 2D drawings and documentation
- **DXF**: 2D CAD interchange

## Data Flow

### Parametric Model Creation

```
User adjusts slider
  ↓
Marimo detects change
  ↓
Reactive cell executes
  ↓
marimocad API called (e.g., mc.box(length, width, height))
  ↓
Core layer validates parameters
  ↓
Check cache for existing result
  ↓ (cache miss)
Backend adapter translates to Build123d
  ↓
Build123d creates geometry
  ↓
Geometry wrapped in marimocad type
  ↓
Result cached
  ↓
Viewer component displays geometry
  ↓
User sees updated 3D model
```

### Boolean Operation

```
User code: mc.subtract(box, cylinder)
  ↓
API validates geometries
  ↓
Core layer unwraps geometry objects
  ↓
Backend adapter performs boolean operation
  ↓
Build123d/CadQuery executes subtract
  ↓
OpenCascade performs BREP operation
  ↓
Result wrapped and returned
  ↓
Cached for future use
```

## Key Design Decisions

### 1. Backend Abstraction

**Decision**: Use protocol-based abstraction with Build123d as primary backend

**Rationale**:
- Allows future backend changes without API breakage
- Build123d offers best Marimo integration
- Protocol typing provides flexibility without inheritance complexity
- Can support multiple backends simultaneously

### 2. Functional API

**Decision**: Primarily function-based rather than object-oriented API

**Rationale**:
- More Pythonic and easier to learn
- Better for interactive/notebook environments
- Simpler to make reactive
- Follows NumPy/SciPy patterns familiar to scientists

**Example**:
```python
# Functional (chosen)
box = mc.box(10, 10, 10)
filleted = mc.fillet(box, 1.0)

# vs. Object-oriented (not chosen)
box = mc.Box(10, 10, 10)
box.fillet(1.0)
```

### 3. Immutable Geometry

**Decision**: Geometry objects are immutable; operations return new objects

**Rationale**:
- Safer for reactive programming
- Easier to cache and optimize
- Prevents accidental mutations
- Clearer data flow

**Example**:
```python
box = mc.box(10, 10, 10)
moved_box = mc.translate(box, x=5)  # box unchanged, new object returned
```

### 4. Lazy Evaluation

**Decision**: Defer expensive operations until results are needed

**Rationale**:
- Better interactive performance
- Can optimize operation chains
- Reduces unnecessary computation
- Better for parameter exploration

### 5. Type Hints

**Decision**: Full type hints for all public APIs using Protocols

**Rationale**:
- Better IDE support and autocomplete
- Catches errors at development time
- Self-documenting code
- Supports multiple backends via duck typing

## Module Structure

```
marimocad/
├── __init__.py              # Package initialization, version
├── geometry.py              # Primitive creation functions
├── operations.py            # Transformations and boolean ops
├── components.py            # Pre-built component library
├── assembly.py              # Assembly management
├── io.py                    # Import/export functions
├── marimo.py                # Marimo-specific integration
├── types.py                 # Type definitions and protocols
├── errors.py                # Custom exceptions
├── backend/
│   ├── __init__.py
│   ├── base.py             # Abstract backend interface
│   ├── build123d.py        # Build123d backend implementation
│   └── cadquery.py         # CadQuery backend implementation
├── core/
│   ├── __init__.py
│   ├── wrapper.py          # Geometry wrapper classes
│   ├── cache.py            # Caching system
│   └── validators.py       # Parameter validation
└── utils/
    ├── __init__.py
    ├── selectors.py         # Selection utilities
    └── helpers.py           # Helper functions
```

## Extension Points

### 1. New Backends

To add a new backend:
1. Implement `Backend` protocol in `backend/`
2. Provide geometry wrapper mappings
3. Register backend in configuration
4. Users can switch: `mc.set_backend("new_backend")`

### 2. Custom Components

Users can create custom components:
```python
def my_component(param1, param2):
    """Custom component."""
    # Use marimocad API
    base = mc.cylinder(param1, param2)
    top = mc.sphere(param1 / 2)
    top = mc.translate(top, z=param2)
    return mc.union(base, top)
```

### 3. Viewer Plugins

Viewer system supports plugins:
```python
class CustomViewer:
    """Custom visualization plugin."""

    def render(self, geometry):
        """Render geometry."""
        # Custom rendering logic
```

## Performance Optimizations

### 1. Geometry Caching

- Cache computed geometries with parameter keys
- LRU cache for memory management
- Invalidation on parameter changes

### 2. Lazy Operation Chains

- Build operation graphs
- Optimize before execution
- Combine redundant operations

### 3. Incremental Updates

- Track which parts of geometry changed
- Only recompute affected regions
- Preserve unchanged subgeometries

### 4. Parallel Execution

- Independent operations can run in parallel
- Batch processing for multiple parts
- Thread pool for concurrent operations

## Testing Strategy

### 1. Unit Tests

- Test each API function independently
- Mock backend for fast testing
- Validate parameter handling
- Test error conditions

### 2. Integration Tests

- Test with real Build123d backend
- Verify geometry correctness
- Test complex operation chains
- Validate exports

### 3. Marimo Integration Tests

- Test reactive behavior
- Verify caching works correctly
- Test viewer integration
- Validate parameter binding

### 4. Performance Tests

- Benchmark operations
- Memory usage profiling
- Cache effectiveness
- Regression testing

## Security Considerations

### 1. File I/O

- Validate file paths
- Sanitize filenames
- Check file sizes before import
- Handle malformed files gracefully

### 2. User Input

- Validate all numeric parameters
- Check for infinity and NaN
- Prevent resource exhaustion
- Limit complexity of operations

### 3. Backend Safety

- Isolate backend errors
- Timeout long operations
- Memory limits for large geometries
- Safe subprocess handling

## Future Architecture Enhancements

### 1. Plugin System

- Loadable plugins for new operations
- Third-party component libraries
- Custom backend implementations
- Viewer extensions

### 2. Cloud Integration

- Remote rendering for complex scenes
- Collaborative editing
- Cloud storage for models
- Shared component libraries

### 3. Analysis Integration

- FEA (Finite Element Analysis) integration
- CFD (Computational Fluid Dynamics) preparation
- Mass properties calculation
- Interference checking

### 4. Version Control

- Model versioning
- Change tracking
- Diff visualization
- Collaborative workflows

### 5. AI/ML Integration

- Generative design
- Topology optimization
- Design suggestions
- Pattern recognition

---

**Document Version**: 1.0
**Last Updated**: 2024-12-15
**Status**: Draft for Review
