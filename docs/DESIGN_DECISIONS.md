# marimocad Design Decisions

## Introduction

This document outlines the key design decisions made during the development of marimocad's API and architecture. Each decision includes the rationale, alternatives considered, and trade-offs.

## 1. Immutable Shape Objects

### Decision
All shape objects in marimocad are immutable. Operations on shapes return new shape instances rather than modifying existing ones.

### Rationale
- **Reactivity**: Marimo's reactive model works best with immutable data structures
- **Predictability**: No hidden state changes; easier to reason about code
- **Thread Safety**: Immutable objects are inherently thread-safe
- **Caching**: Easier to cache results without worrying about mutations
- **History Tracking**: Can maintain operation history without corruption

### Alternatives Considered
1. **Mutable Objects**: Traditional CAD approach where operations modify objects in place
   - Rejected: Conflicts with reactive programming model
   - Rejected: Makes dependency tracking complex
   
2. **Copy-on-Write**: Objects appear mutable but copy internally
   - Rejected: Confusing semantics
   - Rejected: Hidden performance costs

### Trade-offs
- **Pro**: Clean, predictable behavior in reactive contexts
- **Pro**: Easy to implement undo/redo
- **Con**: More memory usage (mitigated by lazy evaluation)
- **Con**: Cannot modify large models in place (mitigated by structural sharing)

### Example
```python
# Immutable approach
box = primitives.box(10, 10, 10)
translated_box = box.translate(x=5)
# 'box' is unchanged, 'translated_box' is a new object

# vs. Mutable approach (rejected)
box = primitives.box(10, 10, 10)
box.translate(x=5)  # Modifies box in place
```

## 2. Fluent Interface with Method Chaining

### Decision
Support method chaining for transformations and operations.

### Rationale
- **Readability**: Natural flow of operations
- **Conciseness**: Reduces intermediate variable clutter
- **Compatibility**: Familiar to users of CadQuery and other CAD libraries
- **Composability**: Easy to build complex operations

### Alternatives Considered
1. **Function Composition**: Using nested function calls
   - Rejected: Less readable for long chains
   
2. **Pipeline Operator**: Wait for Python pipeline operator
   - Rejected: Not yet available in Python

### Trade-offs
- **Pro**: Very readable and intuitive
- **Pro**: Works well with Marimo's cell-based structure
- **Con**: Can become complex with long chains
- **Con**: Type inference can be challenging for IDEs

### Example
```python
result = (box
    .translate(x=10)
    .rotate(axis="Z", angle=45)
    .fillet(edges=result.edges(), radius=2)
    .scale(2))
```

## 3. Context Managers for Complex Construction

### Decision
Use Python context managers (with statements) for sketch-based modeling and assemblies.

### Rationale
- **Pythonic**: Leverages Python's native context manager pattern
- **Scope Management**: Clear boundaries for nested operations
- **State Management**: Implicit state handling without global variables
- **Readability**: Clear hierarchical structure
- **Inspiration**: Similar to build123d's approach

### Alternatives Considered
1. **Explicit Builder Pattern**: Manual builder objects
   - Partial Use: Context managers are a Pythonic builder pattern
   
2. **Pure Functional**: All functional composition
   - Rejected: Too verbose for complex assemblies

### Trade-offs
- **Pro**: Very readable for complex constructions
- **Pro**: Feels natural to Python developers
- **Con**: Requires understanding of context managers
- **Con**: Magic/implicit behavior might confuse beginners

### Example
```python
with BuildPart() as bracket:
    with Sketch(plane="XY") as base:
        base.add_rectangle(width=100, height=60)
    bracket.extrude(distance=5)
```

## 4. Operator Overloading for Boolean Operations

### Decision
Support both operators (+, -, &) and explicit methods (union, subtract, intersect) for boolean operations.

### Rationale
- **Conciseness**: Operators make code more concise
- **Mathematical**: Aligns with set theory notation
- **Flexibility**: Methods provide clearer intent when needed
- **Discoverability**: Methods are easier to find via IDE autocomplete

### Alternatives Considered
1. **Only Operators**: More concise but less discoverable
   - Partial: Operators are primary, methods are aliases
   
2. **Only Methods**: More explicit but verbose
   - Rejected: Too verbose for common operations

### Trade-offs
- **Pro**: Best of both worlds - concise and explicit options
- **Pro**: Intuitive for users familiar with set operations
- **Con**: Two ways to do the same thing (but both clear)

### Example
```python
# Using operators (concise)
result = box1 + box2 - sphere

# Using methods (explicit)
result = box1.union(box2).subtract(sphere)

# Both are valid and equivalent
```

## 5. Lazy Evaluation with Caching

### Decision
Defer expensive geometric operations until results are actually needed, and cache results.

### Rationale
- **Performance**: Avoid unnecessary computations
- **Reactivity**: Better experience in interactive notebooks
- **Memory**: Only store what's needed
- **Composition**: Build complex operations without immediate cost

### Alternatives Considered
1. **Eager Evaluation**: Compute everything immediately
   - Rejected: Poor interactive performance
   
2. **Pure Lazy**: Never cache anything
   - Rejected: Redundant computations

### Trade-offs
- **Pro**: Much better performance for interactive use
- **Pro**: Enables building complex models efficiently
- **Con**: Non-deterministic timing (first access is slow)
- **Con**: Cache management complexity

### Implementation
```python
class Shape:
    def __init__(self):
        self._cached_geometry = None
        self._operation_tree = []
    
    @property
    def geometry(self):
        if self._cached_geometry is None:
            self._cached_geometry = self._evaluate()
        return self._cached_geometry
```

## 6. Reactive Parameter System

### Decision
Integrate with Marimo's reactive system rather than building a custom reactivity layer.

### Rationale
- **Integration**: Seamless experience in Marimo notebooks
- **Simplicity**: Don't reinvent the wheel
- **Familiarity**: Users already understand Marimo's model
- **Maintenance**: Less code to maintain

### Alternatives Considered
1. **Custom Reactivity**: Build own reactive parameter system
   - Rejected: Unnecessary complexity
   - Rejected: Duplicate functionality
   
2. **Observable Pattern**: Implement observer pattern
   - Partial: Used internally, but Marimo integration is primary

### Trade-offs
- **Pro**: Simple and well-integrated
- **Pro**: Leverages Marimo's proven reactivity
- **Con**: Tightly coupled to Marimo (mitigated by optional usage)
- **Con**: Not usable outside Marimo (but that's the use case)

### Example
```python
import marimo as mo

# Marimo handles reactivity
radius = mo.ui.slider(1, 20, value=10)
cylinder = primitives.cylinder(radius=radius.value, height=20)
# Automatically updates when slider changes
```

## 7. Type Hints Throughout

### Decision
Use comprehensive type hints for all public APIs.

### Rationale
- **IDE Support**: Better autocomplete and inline documentation
- **Type Safety**: Catch errors before runtime
- **Documentation**: Types serve as documentation
- **Modern Python**: Aligns with Python 3.9+ best practices

### Alternatives Considered
1. **No Type Hints**: More flexible but less safe
   - Rejected: Type hints are standard in modern Python
   
2. **Gradual Typing**: Add types over time
   - Rejected: Start with types from the beginning

### Trade-offs
- **Pro**: Much better developer experience
- **Pro**: Catches bugs early with mypy
- **Con**: More verbose code
- **Con**: Can be complex for generic/union types

### Example
```python
def box(
    width: float,
    height: float,
    depth: float,
    center: bool = True
) -> Shape3D:
    """Create a box shape."""
    ...
```

## 8. OpenCASCADE as Primary Geometry Kernel

### Decision
Use OpenCASCADE (via OCP Python bindings) as the primary geometry kernel.

### Rationale
- **Industry Standard**: Proven, mature CAD kernel
- **Capabilities**: Full BREP modeling, NURBS, advanced operations
- **File Formats**: Native STEP, IGES support
- **Community**: Large user base and extensive documentation
- **Reliability**: Battle-tested in commercial applications

### Alternatives Considered
1. **CGAL**: Computational geometry algorithms library
   - Partial: May use for specific algorithms
   - Rejected as primary: Less CAD-focused
   
2. **Custom Kernel**: Build lightweight custom kernel
   - Rejected: Massive undertaking
   - Rejected: Unlikely to match OCC quality
   
3. **Multiple Backends**: Support multiple kernels
   - Future: Possible plugin architecture
   - Initial: Too complex for v1

### Trade-offs
- **Pro**: Professional-grade geometric capabilities
- **Pro**: Standard file format support
- **Con**: Large dependency (~100MB+)
- **Con**: Complex C++ bindings
- **Con**: Steep learning curve for contributors

## 9. Three.js for Visualization

### Decision
Use Three.js as the primary 3D rendering engine.

### Rationale
- **Popularity**: Most widely used WebGL library
- **Performance**: Hardware-accelerated, efficient
- **Features**: Rich set of rendering features
- **Documentation**: Excellent docs and examples
- **Ecosystem**: Large ecosystem of plugins and tools
- **Marimo Compatibility**: Works well in web environment

### Alternatives Considered
1. **Babylon.js**: More feature-rich, heavier
   - Alternative: Support as optional backend
   
2. **WebGL Direct**: Maximum performance
   - Rejected: Too low-level, reinventing wheel
   
3. **VTK.js**: Scientific visualization focus
   - Considered: May use for specific features

### Trade-offs
- **Pro**: Best balance of features and performance
- **Pro**: Easy to customize and extend
- **Con**: Requires tessellation of BREP surfaces
- **Con**: Limited to web environments (but that's the target)

## 10. Progressive Rendering Strategy

### Decision
Implement progressive rendering for large models: start with low-resolution mesh, refine incrementally.

### Rationale
- **Responsiveness**: Immediate feedback, even for large models
- **User Experience**: Better than blocking/freezing
- **Perception**: Feels faster even if total time is similar
- **Interactivity**: User can interact while refining

### Alternatives Considered
1. **Blocking Render**: Wait for full quality
   - Rejected: Poor UX for large models
   
2. **Fixed LOD**: Single level of detail
   - Rejected: Can't handle wide range of model sizes

### Trade-offs
- **Pro**: Much better UX for large models
- **Pro**: Enables working with more complex geometry
- **Con**: Implementation complexity
- **Con**: May show artifacts during refinement

## 11. Selector Syntax for Topology

### Decision
Use string-based selector syntax for filtering faces, edges, and vertices (e.g., ">Z", "|X").

### Rationale
- **Conciseness**: Very compact notation
- **Expressiveness**: Can express complex selections simply
- **Familiarity**: Used by CadQuery, proven effective
- **Readability**: Once learned, very readable

### Selector Syntax
- `>X`: Faces/edges pointing in +X direction
- `<X`: Faces/edges pointing in -X direction
- `|X`: Faces/edges parallel to X axis
- `#X`: Faces/edges perpendicular to X axis

### Alternatives Considered
1. **Predicate Functions**: Lambda-based filtering
   - Partial: Support both for flexibility
   
2. **Method Chaining**: .filter().by_direction(), etc.
   - Rejected: Too verbose

### Trade-offs
- **Pro**: Very concise and expressive
- **Pro**: Works well with fluent interface
- **Con**: Learning curve for new users
- **Con**: Limited to common cases (use predicates for complex cases)

### Example
```python
# Fillet top edges
box.fillet(edges=box.edges(">Z"), radius=2)

# Chamfer vertical edges
box.chamfer(edges=box.edges("|Z"), distance=1)
```

## 12. Assembly as First-Class Concept

### Decision
Treat assemblies as first-class objects, not just collections of shapes.

### Rationale
- **Real-World**: Most CAD work involves assemblies
- **Constraints**: Need to manage relationships between parts
- **Export**: STEP assemblies preserve structure
- **Organization**: Natural way to organize complex models

### Alternatives Considered
1. **Flat Collections**: Just lists of shapes
   - Rejected: Loses structure and relationships
   
2. **Scene Graph**: Generic hierarchical structure
   - Partial: Assembly internally uses scene graph

### Trade-offs
- **Pro**: Matches real-world CAD workflows
- **Pro**: Better organization for complex projects
- **Con**: More API surface area
- **Con**: Additional complexity

### Example
```python
assembly = Assembly(name="motor")
assembly.add_part("base", base_plate)
assembly.add_part("mount", mount, position=(0, 0, 10))
assembly.export_step("motor.step")
```

## 13. File Format Support

### Decision
Support STEP and IGES for precise CAD interchange, STL/OBJ/GLTF for visualization/manufacturing.

### Rationale
- **STEP**: Industry standard for CAD data exchange
- **IGES**: Legacy but still widely used
- **STL**: De facto standard for 3D printing
- **OBJ**: Simple, universal mesh format
- **GLTF**: Modern format for web/visualization

### Alternatives Considered
1. **Minimal Formats**: Only STL
   - Rejected: Too limiting
   
2. **All Formats**: Support every CAD format
   - Rejected: Maintenance burden
   - Future: Add more formats as needed

### Trade-offs
- **Pro**: Covers common use cases
- **Pro**: Balance between capability and complexity
- **Con**: Users might need other formats
- **Con**: Each format has maintenance cost

## 14. Error Handling Strategy

### Decision
Use custom exception hierarchy with meaningful error messages and recovery suggestions.

### Rationale
- **User Experience**: Help users fix problems
- **Debugging**: Clear error messages save time
- **Type Safety**: Specific exceptions for specific errors
- **Robustness**: Graceful degradation when possible

### Exception Hierarchy
```
MarimoCADError (base)
├── GeometryError
│   ├── InvalidOperationError
│   ├── TopologyError
│   └── DegenerateGeometryError
├── VisualizationError
│   ├── MeshGenerationError
│   └── RenderError
├── IOError
│   ├── ImportError
│   └── ExportError
└── ParameterError
```

### Alternatives Considered
1. **Generic Exceptions**: Use built-in exceptions
   - Rejected: Less informative
   
2. **Return Codes**: Return None or error codes
   - Rejected: Not Pythonic

### Trade-offs
- **Pro**: Better user experience
- **Pro**: Easier to handle specific errors
- **Con**: More exception classes to maintain

## 15. Component-Based Modeling

### Decision
Support component classes that encapsulate parametric logic.

### Rationale
- **Reusability**: Define once, use many times
- **Organization**: Logical grouping of related geometry
- **Encapsulation**: Hide implementation details
- **Parametric**: Natural way to express parametric models
- **Object-Oriented**: Familiar to Python developers

### Alternatives Considered
1. **Pure Functional**: Just functions
   - Partial: Functions work too, components are optional
   
2. **Macro System**: Record and replay operations
   - Future: Possible addition

### Trade-offs
- **Pro**: Very powerful for complex parametric models
- **Pro**: Encourages good code organization
- **Con**: More advanced concept, steeper learning curve
- **Con**: Overkill for simple models

### Example
```python
class CustomBracket(Component):
    def __init__(self, width, height, thickness):
        self.width = width
        self.height = height
        self.thickness = thickness
    
    def build(self):
        # Component logic here
        return shape
```

## Summary of Key Principles

1. **Reactivity First**: Design for reactive programming from the ground up
2. **Pythonic**: Use Python idioms and patterns naturally
3. **Type Safe**: Comprehensive type hints for better DX
4. **Immutable**: Immutable data structures for predictability
5. **Performant**: Lazy evaluation and caching for speed
6. **Extensible**: Plugin-ready architecture for future growth
7. **Standards-Based**: Use industry-standard formats and kernels
8. **User-Friendly**: Clear API, good errors, helpful documentation

## Future Considerations

### Potential Changes
1. **Plugin System**: Allow third-party extensions
2. **Cloud Backend**: Server-side rendering for heavy models
3. **Multiple Kernels**: Support alternative geometry engines
4. **Constraint Solver**: Geometric constraints for sketches
5. **FEA Integration**: Finite element analysis capabilities
6. **Version Control**: Built-in versioning for models
7. **Collaboration**: Real-time multi-user editing

### Evolution Strategy
- Maintain backward compatibility where possible
- Use deprecation warnings for API changes
- Version APIs (v1, v2) if breaking changes needed
- Community feedback drives priorities

## Conclusion

These design decisions collectively create an API and architecture that is:
- **Natural** for Marimo users
- **Powerful** for CAD modeling
- **Performant** for interactive use
- **Extensible** for future growth

The decisions prioritize user experience and integration with Marimo while maintaining the power and flexibility needed for serious CAD work. Trade-offs were carefully considered, with a bias toward simplicity and usability for the common case while supporting advanced use cases where needed.
