# marimocad Design Decisions

This document explains the key design decisions made during the development of marimocad's API and architecture.

## Decision Summary

| Decision | Status | Impact |
|----------|--------|--------|
| Build123d as primary backend | ✅ Approved | High |
| Functional API design | ✅ Approved | High |
| Immutable geometry | ✅ Approved | Medium |
| Protocol-based type system | ✅ Approved | Medium |
| Lazy evaluation | ✅ Approved | Medium |
| Backend abstraction layer | ✅ Approved | High |

## 1. Backend Selection: Build123d

### Decision

Use Build123d as the primary CAD backend with CadQuery as an optional secondary backend.

### Context

We evaluated three Python CAD libraries:
- **Build123d**: Modern Python CAD library with native notebook support
- **CadQuery**: Mature fluent API library with large community
- **pythonOCC (OCP)**: Low-level OpenCascade Python bindings

### Rationale

**Build123d chosen because:**

1. **Native Marimo Integration**
   - Built-in `_repr_html_()` for automatic rendering
   - Works seamlessly in notebooks without extra configuration
   - No external viewer required for basic visualization

2. **Modern Python API**
   - Context managers (Pythonic)
   - Type hints throughout
   - Multiple modeling paradigms (Builder, Algebra, Direct)
   - Better alignment with Python 3.9+ idioms

3. **Superior Selectors**
   - More powerful filtering system
   - Intuitive chaining
   - Better performance for complex selections

4. **Active Development**
   - Regular updates and improvements
   - Responsive maintainer
   - Modern features added continuously

5. **Flexible Architecture**
   - Multiple ways to model (builder vs. algebra vs. direct)
   - Users can choose their preferred style
   - Easier to create abstractions

**CadQuery as Secondary:**
- Excellent documentation
- Large community
- More mature and stable
- Good fallback if Build123d has issues

**pythonOCC Rejected:**
- Too low-level for user-facing API
- Poor developer experience
- Both other libraries use it under the hood

### Consequences

**Positive:**
- Best notebook experience
- Modern, maintainable codebase
- Flexible modeling approaches
- Good performance

**Negative:**
- Smaller community than CadQuery
- Less mature (may have undiscovered bugs)
- API may still evolve
- Fewer third-party tutorials

### Alternatives Considered

1. **CadQuery as primary**: Rejected due to lack of native notebook rendering
2. **Direct OCP**: Rejected due to verbosity and poor UX
3. **Multiple backends equally**: Rejected as too complex to maintain

### References

- [CAD_LIBRARY_COMPARISON.md](CAD_LIBRARY_COMPARISON.md)
- [RESEARCH_SUMMARY.md](RESEARCH_SUMMARY.md)
- Build123d documentation: https://build123d.readthedocs.io/

---

## 2. API Style: Functional vs. Object-Oriented

### Decision

Use a primarily functional API with functions that return new geometry objects.

### Context

We considered three API styles:
1. **Functional**: `result = mc.fillet(box, radius=1.0)`
2. **Object-Oriented**: `box.fillet(1.0)` (modifies in place)
3. **Fluent/Chaining**: `box.fillet(1.0).translate(5, 0, 0)`

### Rationale

**Functional chosen because:**

1. **Better for Reactive Programming**
   - Clear data flow: input → function → output
   - No hidden state mutations
   - Easier for Marimo to track dependencies
   - More predictable behavior

2. **Immutability**
   - Original geometry preserved
   - Can reuse intermediate results
   - Safer for concurrent operations
   - Easier to debug

3. **Pythonic for Scientific Computing**
   - Follows NumPy/SciPy patterns
   - Familiar to data scientists
   - Consistent with functional programming trends
   - Type hints work better

4. **Composability**
   - Functions can be easily combined
   - Higher-order functions possible
   - Better for building abstractions

5. **Testing**
   - Pure functions easier to test
   - No setup/teardown needed
   - Deterministic behavior

**Example:**
```python
# Functional (chosen)
box = mc.box(10, 10, 10)
filleted = mc.fillet(box, radius=1.0)
moved = mc.translate(filleted, x=5)

# Both box and filleted still exist unchanged
assert box != filleted
assert filleted != moved
```

vs.

```python
# Object-oriented (not chosen)
box = mc.Box(10, 10, 10)
box.fillet(1.0)  # Modifies box in place
box.translate(5, 0, 0)  # Original box lost

# Can't access intermediate states
```

### Consequences

**Positive:**
- Safer and more predictable
- Better IDE support
- Easier to understand data flow
- Works well with Marimo

**Negative:**
- Slightly more verbose
- Can't chain operations naturally
- May create many intermediate variables

### Mitigation

For users who prefer chaining, we provide a fluent wrapper:

```python
# Optional fluent API
from marimocad.fluent import Geometry

result = (Geometry(mc.box(10, 10, 10))
    .fillet(1.0)
    .translate(x=5)
    .get())
```

### Alternatives Considered

1. **Pure OOP**: Rejected - harder to make reactive and immutable
2. **Fluent API**: Rejected as primary - less clear data flow
3. **Hybrid**: Considered but rejected as confusing

---

## 3. Type System: Protocols vs. Inheritance

### Decision

Use Protocol-based duck typing instead of classical inheritance for geometry types.

### Context

Python 3.8+ supports structural subtyping via `typing.Protocol`, which allows type checking based on interface rather than inheritance.

### Rationale

**Protocols chosen because:**

1. **Backend Flexibility**
   - Don't need to wrap every backend object
   - Can work with Build123d objects directly
   - Easier to add new backends
   - No forced inheritance hierarchy

2. **Duck Typing**
   - Pythonic approach
   - "If it walks like a duck..."
   - Less rigid than inheritance
   - Better for evolution

3. **Type Safety**
   - Still get static type checking
   - IDE autocomplete works
   - MyPy can verify correctness
   - No runtime overhead

4. **Simplicity**
   - Less boilerplate code
   - No wrapper classes needed
   - Easier to understand
   - Fewer abstractions

**Example:**
```python
# Protocol-based (chosen)
from typing import Protocol

class Geometry(Protocol):
    """Any object with these methods is a Geometry."""
    def bounding_box(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]: ...
    def center(self) -> tuple[float, float, float]: ...

# Build123d objects already satisfy this protocol
from build123d import Box
box = Box(10, 10, 10)  # This IS a Geometry (duck typing)

def translate(geom: Geometry, x: float, y: float, z: float) -> Geometry:
    # Works with any object implementing the protocol
    pass
```

vs.

```python
# Inheritance-based (not chosen)
class Geometry(ABC):
    @abstractmethod
    def bounding_box(self): ...

class WrappedBuild123dGeometry(Geometry):
    def __init__(self, build123d_obj):
        self._obj = build123d_obj  # Need to wrap everything
    
    def bounding_box(self):
        return self._obj.bounding_box()  # Delegate to wrapped object
```

### Consequences

**Positive:**
- Less code to write and maintain
- More flexible
- Better performance (no wrapper overhead)
- Easier backend integration

**Negative:**
- Less explicit inheritance hierarchy
- May be unfamiliar to some developers
- Requires Python 3.8+

### Alternatives Considered

1. **Abstract Base Classes**: Rejected - too rigid, requires wrapping
2. **No types**: Rejected - lose IDE support and type safety
3. **Union types**: Considered but rejected as too permissive

---

## 4. Geometry Mutability: Immutable Objects

### Decision

All geometry objects are immutable. Operations return new objects rather than modifying in place.

### Context

In CAD, operations like fillet or translate could either:
1. Modify the geometry in place
2. Return a new geometry (immutable)

### Rationale

**Immutability chosen because:**

1. **Reactive Programming**
   - Marimo needs to detect changes
   - Immutable objects make this trivial
   - No hidden side effects
   - Clear dependency tracking

2. **Safety**
   - Can't accidentally modify shared geometry
   - Thread-safe by default
   - No defensive copying needed
   - Easier to reason about

3. **Caching**
   - Can cache aggressively
   - Don't worry about invalidation
   - Better performance for repeated operations
   - Simpler cache implementation

4. **Debugging**
   - Can inspect intermediate states
   - History preserved naturally
   - Easier to reproduce bugs
   - Better error messages

5. **Functional Programming**
   - Aligns with functional API
   - Composable operations
   - Referential transparency
   - Easier testing

**Example:**
```python
# Immutable (chosen)
original_box = mc.box(10, 10, 10)
filleted_box = mc.fillet(original_box, radius=1.0)

# Both exist independently
assert original_box is not filleted_box
mc.export_step(original_box, "original.step")
mc.export_step(filleted_box, "filleted.step")

# Can reuse original_box
chamfered_box = mc.chamfer(original_box, distance=0.5)
```

vs.

```python
# Mutable (not chosen)
box = mc.box(10, 10, 10)
box.fillet(1.0)  # Modifies box

# Original box is lost
# Can't access pre-fillet state
# Harder to track in reactive environment
```

### Consequences

**Positive:**
- Safer code
- Better for reactive programming
- Easier caching
- Natural version history

**Negative:**
- More memory usage (stores multiple versions)
- May be slower for long operation chains
- Different from some CAD tools

### Mitigation

- Implement copy-on-write for efficiency
- Cache results to avoid recomputation
- Provide guidance on memory management

### Alternatives Considered

1. **Mutable objects**: Rejected - conflicts with reactive model
2. **Copy-on-write**: Implemented as optimization
3. **Explicit copy()**: Unnecessary with immutability

---

## 5. Error Handling Strategy

### Decision

Use custom exception hierarchy with descriptive messages rather than returning None or error codes.

### Context

Operations can fail (invalid parameters, geometric impossibility, etc.). Need to decide how to communicate errors.

### Rationale

**Exceptions chosen because:**

1. **Pythonic**
   - Standard Python error handling
   - Can't ignore errors accidentally
   - Stack traces for debugging
   - Natural control flow

2. **Descriptive Messages**
   - Can provide detailed context
   - Help users fix problems
   - Include parameter values
   - Suggest solutions

3. **Typed Exceptions**
   - Can catch specific errors
   - Different handling for different errors
   - Better error recovery
   - Clear error categories

4. **Integration**
   - Works well with Marimo
   - IDE can show error types
   - Standard try/except syntax
   - Good logging support

**Exception Hierarchy:**
```python
class MarimoCADError(Exception):
    """Base exception for all marimocad errors."""

class GeometryError(MarimoCADError):
    """Raised when geometry operation fails."""

class ParameterError(MarimoCADError):
    """Raised for invalid parameters."""

class ExportError(MarimoCADError):
    """Raised when export fails."""

class ImportError(MarimoCADError):
    """Raised when import fails."""

class ConstraintError(MarimoCADError):
    """Raised when constraint solving fails."""
```

**Example:**
```python
try:
    box = mc.box(-10, 20, 30)  # Negative dimension
except mc.ParameterError as e:
    print(f"Invalid parameter: {e}")
    # Error message: "Box length must be positive, got -10"

try:
    tiny_box = mc.box(0.001, 0.001, 0.001)
    mc.fillet(tiny_box, radius=10.0)  # Fillet too large
except mc.GeometryError as e:
    print(f"Geometry operation failed: {e}")
    # Error message: "Fillet radius 10.0 exceeds edge length 0.001"
```

### Consequences

**Positive:**
- Clear error communication
- Standard Python patterns
- Good debugging experience
- Explicit error handling

**Negative:**
- Requires try/except for recovery
- May interrupt execution
- Need to document exceptions

### Alternatives Considered

1. **Return None**: Rejected - easy to ignore, unclear cause
2. **Return Result[T, Error]**: Rejected - not Pythonic
3. **Log and continue**: Rejected - hides problems

---

## 6. Lazy Evaluation Strategy

### Decision

Use lazy evaluation for complex operation chains with optional eager evaluation.

### Context

CAD operations can be expensive. Should we:
1. Execute immediately (eager)
2. Defer until needed (lazy)
3. Hybrid approach

### Rationale

**Lazy evaluation chosen because:**

1. **Performance**
   - Avoid unnecessary computation
   - Can optimize operation chains
   - Better for parameter exploration
   - Faster interactive response

2. **Optimization Opportunities**
   - Combine redundant operations
   - Reorder for efficiency
   - Cancel out inverse operations
   - Batch similar operations

3. **Memory Efficiency**
   - Don't store intermediate results
   - Generate on demand
   - Better for large models
   - Reduced memory footprint

4. **Interactive Use**
   - Faster initial response
   - Compute only what's displayed
   - Better for notebooks
   - Smoother user experience

**Implementation:**
```python
# Lazy by default
box = mc.box(10, 10, 10)  # Not computed yet
filleted = mc.fillet(box, 1.0)  # Still not computed

# Computed when needed
mc.viewer(filleted)  # Now computes
mc.export_step(filleted, "part.step")  # Computes if not cached

# Force eager evaluation if needed
result = mc.evaluate(filleted)  # Explicitly compute
```

### Consequences

**Positive:**
- Better performance
- Optimization opportunities
- Memory efficient
- Good interactive experience

**Negative:**
- More complex implementation
- Errors appear later
- Harder to debug
- May confuse users

### Mitigation

- Clear documentation
- Provide eager mode option
- Good error messages showing operation chain
- Debugging tools to inspect lazy operations

### Alternatives Considered

1. **Fully eager**: Rejected - too slow for interactive use
2. **Fully lazy**: Rejected - errors too delayed
3. **Hybrid (chosen)**: Best balance

---

## 7. Visualization Approach

### Decision

Use ocp-vscode as primary 3D viewer with fallback to SVG projections.

### Context

Need to display 3D models in Marimo notebooks. Options:
1. ocp-vscode (WebGL viewer)
2. Three.js custom viewer
3. SVG projections
4. External applications

### Rationale

**ocp-vscode chosen because:**

1. **Native Integration**
   - Built for OpenCascade
   - Works with Build123d
   - Already installed by users
   - No extra dependencies

2. **Feature Rich**
   - 3D rotation/pan/zoom
   - Multiple view modes
   - Measurements
   - Section views
   - Assembly explosion

3. **Performance**
   - WebGL acceleration
   - Handles large models
   - Smooth interaction
   - Good rendering quality

4. **Notebook Friendly**
   - Designed for Jupyter/IPython
   - Works in Marimo
   - No separate window
   - Inline display

**SVG as Fallback:**
- Works without JavaScript
- Good for documentation
- Can export images
- Lighter weight

**Example:**
```python
# 3D viewer (primary)
box = mc.box(10, 10, 10)
mc.viewer(box)  # Interactive 3D

# 2D projection (fallback)
mc.viewer(box, mode="svg", view="iso")  # Static SVG
```

### Consequences

**Positive:**
- Rich 3D visualization
- Good performance
- Feature complete
- Well maintained

**Negative:**
- Requires JavaScript
- External dependency
- May not work in all environments

### Mitigation

- Provide SVG fallback
- Clear documentation
- Detect environment capabilities
- Graceful degradation

### Alternatives Considered

1. **Custom Three.js viewer**: Rejected - too much work
2. **VTK**: Rejected - heavyweight
3. **External apps**: Rejected - poor notebook integration

---

## 8. Component Library Organization

### Decision

Organize components by domain (mechanical, structural, electrical) with parametric functions.

### Context

Need to provide pre-built components (screws, gears, etc.). How to organize?

### Rationale

**Domain-based organization chosen because:**

1. **Discoverability**
   - Users think in domains
   - Clear categorization
   - Easier to find components
   - Logical grouping

2. **Extensibility**
   - Easy to add new domains
   - Third-party extensions
   - User contributions
   - Plugin system possible

3. **Documentation**
   - Natural documentation structure
   - Domain-specific examples
   - Reference by category
   - Better learning path

**Structure:**
```python
marimocad.components.mechanical:
  - screw()
  - nut()
  - bolt()
  - gear()
  - bearing()
  - spring()

marimocad.components.structural:
  - i_beam()
  - channel()
  - angle()
  - tube()

marimocad.components.electrical:
  - enclosure()
  - din_rail()
  - terminal_block()

marimocad.components.custom:
  - User-defined components
```

### Consequences

**Positive:**
- Clear organization
- Easy to navigate
- Extensible
- Well-documented

**Negative:**
- Some components fit multiple categories
- Need to maintain taxonomy
- May need cross-references

### Alternatives Considered

1. **Flat namespace**: Rejected - too many components
2. **By standard (ISO, DIN)**: Rejected - too technical
3. **Alphabetical**: Rejected - hard to discover

---

## Summary

These design decisions create a foundation for a powerful, flexible, and user-friendly CAD library for Marimo notebooks. Key themes:

1. **Modern Python**: Leverage latest Python features
2. **Reactive First**: Designed for Marimo from ground up
3. **Safety**: Immutability and type safety
4. **Performance**: Lazy evaluation and caching
5. **Flexibility**: Multiple backends and paradigms
6. **Usability**: Clear API and good error messages

## Review and Updates

These decisions should be reviewed:
- After major backend updates
- When user feedback suggests issues
- When new Python features become available
- When Marimo adds relevant features

---

**Document Version**: 1.0
**Last Updated**: 2024-12-15
**Status**: Approved for Implementation
**Next Review**: After v0.1.0 release
