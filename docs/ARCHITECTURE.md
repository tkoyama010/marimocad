# marimocad Architecture

## Overview

marimocad is built on a layered architecture that integrates CAD geometry manipulation with Marimo's reactive programming model. The architecture is designed to be modular, extensible, and performant while maintaining a clean separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Marimo Notebook Layer                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  User Interface (Marimo Cells)                                     │  │
│  │  - Interactive sliders, inputs, and controls                       │  │
│  │  - Reactive parameter binding                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        marimocad API Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Primitives  │  │   Boolean    │  │ Transformatio│  │  Assembly  │  │
│  │   Module     │  │  Operations  │  │   Module     │  │   Module   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Sketch     │  │ Modification │  │     I/O      │  │Measurement │  │
│  │   Module     │  │   Module     │  │   Module     │  │   Module   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Reactive Core Layer                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Shape Graph Manager                                               │  │
│  │  - Dependency tracking between shapes                              │  │
│  │  - Automatic propagation of parameter changes                      │  │
│  │  - Lazy evaluation and caching                                     │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Parameter Manager                                                 │  │
│  │  - Reactive parameter storage                                      │  │
│  │  - Change notification system                                      │  │
│  │  - Validation and constraints                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Geometry Engine Layer                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Shape Classes (Shape, Shape2D, Shape3D)                          │  │
│  │  - Immutable shape objects                                         │  │
│  │  - Operation history and provenance                                │  │
│  │  - Topology and geometry data                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Topological Operations                                            │  │
│  │  - Face, edge, vertex selection and filtering                      │  │
│  │  - Topological queries                                             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Visualization Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │  Three.js    │  │   Babylon.js │  │   WebGL      │                  │
│  │  Renderer    │  │   Renderer   │  │   Direct     │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Mesh Generation and Tessellation                                 │  │
│  │  - Adaptive mesh refinement                                        │  │
│  │  - LOD (Level of Detail) management                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CAD Kernel Layer (Optional)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ OpenCASCADE  │  │   CGAL       │  │   Custom     │                  │
│  │   (OCP)      │  │   Binding    │  │   Kernel     │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│  - BREP solid modeling                                                  │
│  - Boolean operations (union, difference, intersection)                 │
│  - Advanced surface operations                                          │
│  - Import/Export (STEP, IGES, STL, etc.)                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Marimo Notebook Layer

**Purpose**: User-facing interface for interactive CAD modeling

**Components**:
- Interactive UI controls (sliders, inputs, dropdowns)
- Reactive cell execution
- Parameter binding to CAD objects
- Real-time visualization updates

**Key Features**:
- Automatic dependency tracking through Marimo
- No manual refresh needed
- Live preview as parameters change
- Notebook-native 3D viewer

### 2. marimocad API Layer

**Purpose**: High-level API for CAD operations

**Modules**:

#### Primitives Module
- Basic 2D shapes (circle, rectangle, polygon, ellipse)
- Basic 3D shapes (box, sphere, cylinder, cone, torus)
- Factory functions for shape creation

#### Boolean Operations Module
- Union (addition)
- Subtraction (difference)
- Intersection
- Operator overloading (+, -, &)

#### Transformation Module
- Translation, rotation, scaling
- Mirroring
- Matrix transformations
- Chained transformations

#### Sketch Module
- 2D sketch creation
- Profile building
- Extrusion and revolution
- Context manager support

#### Modification Module
- Filleting and chamfering
- Shelling and offsetting
- Edge and face selection
- Advanced surface operations

#### Assembly Module
- Multi-part assemblies
- Positional constraints
- Component hierarchies
- Assembly-level operations

#### I/O Module
- STEP, IGES import/export
- STL, OBJ export
- Native format serialization
- Format conversion utilities

#### Measurement Module
- Volume and area calculations
- Center of mass
- Bounding boxes
- Distance and intersection queries

### 3. Reactive Core Layer

**Purpose**: Manage reactivity and dependency tracking

**Components**:

#### Shape Graph Manager
```python
class ShapeGraph:
    """Manages dependency graph of shapes."""
    
    def __init__(self):
        self.nodes = {}  # shape_id -> node
        self.edges = {}  # shape_id -> [dependent_shape_ids]
        self.cache = {}  # shape_id -> computed_result
    
    def add_dependency(self, parent, child):
        """Add dependency relationship."""
        
    def invalidate(self, shape_id):
        """Invalidate cache for shape and dependents."""
        
    def evaluate(self, shape_id):
        """Evaluate shape with dependency resolution."""
```

#### Parameter Manager
```python
class ParameterManager:
    """Manages reactive parameters."""
    
    def __init__(self):
        self.parameters = {}
        self.observers = {}
    
    def set_parameter(self, name, value):
        """Set parameter and notify observers."""
        
    def observe(self, param_name, callback):
        """Register callback for parameter changes."""
```

**Key Features**:
- Directed Acyclic Graph (DAG) for shape dependencies
- Lazy evaluation with caching
- Automatic invalidation on parameter changes
- Observable parameter system

### 4. Geometry Engine Layer

**Purpose**: Core geometric representations and operations

**Components**:

#### Shape Base Classes
```python
class Shape:
    """Immutable base class for all shapes."""
    
    def __init__(self, geometry_data, parameters, operation_history):
        self._geometry = geometry_data
        self._params = parameters
        self._history = operation_history
    
    def __add__(self, other):
        """Union operation."""
        return self.union(other)
    
    def __sub__(self, other):
        """Subtraction operation."""
        return self.subtract(other)
```

#### Topological Data Structures
- **Vertex**: Point in 3D space
- **Edge**: Connection between two vertices (curve)
- **Face**: Bounded surface
- **Shell**: Collection of connected faces
- **Solid**: Volume enclosed by shells

**Key Features**:
- Immutable shape objects (functional style)
- Full operation history for provenance
- Efficient topology queries
- BREP (Boundary Representation) model

### 5. Visualization Layer

**Purpose**: Render 3D CAD models in the browser

**Components**:

#### Mesh Generator
- Tessellation of BREP surfaces
- Adaptive refinement based on curvature
- LOD (Level of Detail) generation
- Normal and UV coordinate generation

#### Renderer Backends
- **Three.js**: Primary renderer (lightweight, popular)
- **Babylon.js**: Alternative (more features)
- **WebGL Direct**: For maximum performance

#### Interactive Controls
- Orbit camera controls
- Pan and zoom
- Object selection
- Measuring tools

**Key Features**:
- Progressive rendering for large models
- Hardware acceleration via WebGL
- Responsive and smooth interaction
- Export to various image formats

### 6. CAD Kernel Layer

**Purpose**: Low-level geometric computation

**Primary Option: OpenCASCADE (via OCP)**
- Industry-standard CAD kernel
- Full BREP modeling capabilities
- Advanced surface operations
- Proven reliability

**Alternative Options**:
- CGAL for computational geometry algorithms
- Custom lightweight kernel for basic operations

**Key Features**:
- Robust boolean operations
- NURBS surface support
- Standard file format support
- High precision calculations

## Data Flow

### Creating and Visualizing a Shape

```
1. User Code:
   box = primitives.box(10, 10, 10)

2. API Layer:
   - primitives.box() called
   - Creates Shape3D object

3. Reactive Core:
   - Registers shape in graph
   - No evaluation yet (lazy)

4. User Code:
   viewer = visualize(box)

5. Visualization Layer:
   - Requests geometry data
   - Triggers evaluation in Geometry Engine
   - Geometry Engine calls CAD Kernel
   - CAD Kernel returns BREP data
   - Mesh Generator tessellates surfaces
   - Renderer displays in browser

6. Cache:
   - Result cached for reuse
```

### Reactive Parameter Update

```
1. User Interaction:
   - Slider moved (radius changed)

2. Marimo Layer:
   - Detects parameter change
   - Triggers cell re-execution

3. Reactive Core:
   - ParameterManager notifies observers
   - ShapeGraph invalidates cache for dependent shapes

4. API Layer:
   - New shape created with updated parameter

5. Visualization Layer:
   - Automatically re-renders with new geometry
   - Uses cached results where possible
```

## Design Patterns

### 1. Immutable Objects
All shape objects are immutable. Operations return new shapes rather than modifying existing ones. This ensures:
- Thread safety
- Predictable behavior in reactive contexts
- Easy caching and memoization

### 2. Fluent Interface
Chained operations for readable code:
```python
result = (box
    .translate(x=10)
    .rotate(axis="Z", angle=45)
    .fillet(edges=result.edges(), radius=2))
```

### 3. Context Managers
For complex constructions:
```python
with BuildPart() as part:
    with Sketch() as profile:
        profile.add_circle(radius=10)
    part.extrude(distance=20)
```

### 4. Observer Pattern
For reactive parameter updates:
- Parameters are observable
- Shapes register as observers
- Automatic notification on changes

### 5. Lazy Evaluation
Expensive operations deferred until needed:
- Boolean operations computed on demand
- Mesh generation only when visualizing
- Caching of computed results

### 6. Factory Pattern
Shape creation through factory functions:
```python
primitives.box(10, 10, 10)
primitives.sphere(radius=5)
```

## Technology Stack

### Core Dependencies

- **Python 3.9+**: Modern Python features (type hints, dataclasses)
- **NumPy**: Numerical computations and array operations
- **OCP (OpenCASCADE Python)**: CAD kernel bindings
- **Marimo**: Reactive notebook environment

### Visualization Dependencies

- **Three.js**: 3D rendering in browser
- **pythreejs** or **custom wrapper**: Python bindings for Three.js
- **Jupyter Widgets**: Interactive controls (fallback)

### Optional Dependencies

- **CGAL**: Computational geometry algorithms
- **Trimesh**: Mesh processing utilities
- **NetworkX**: Graph operations for dependencies

### Development Tools

- **pytest**: Testing framework
- **mypy**: Static type checking
- **black**: Code formatting
- **sphinx**: Documentation generation

## Performance Optimization

### 1. Caching Strategy
- **Shape Cache**: Store computed geometry
- **Mesh Cache**: Store generated meshes
- **Invalidation**: Smart cache invalidation on parameter changes

### 2. Lazy Evaluation
- Defer expensive operations
- Compute only what's needed
- Batch operations when possible

### 3. Progressive Rendering
- Load and display models incrementally
- Start with low-resolution mesh
- Refine progressively

### 4. Multi-threading
- Geometry operations in background threads
- Non-blocking visualization updates
- Parallel mesh generation

### 5. Memory Management
- Automatic cleanup of unused shapes
- Reference counting
- Weak references for caches

## Extensibility

### Plugin System
Future plugin architecture for:
- Custom primitives
- New file formats
- Alternative renderers
- Domain-specific operations

### Extension Points
```python
# Custom primitive
@register_primitive
def custom_gear(teeth, module, pressure_angle):
    # Implementation
    return shape

# Custom operation
@register_operation
def custom_twist(shape, angle):
    # Implementation
    return twisted_shape

# Custom renderer
@register_renderer("custom")
class CustomRenderer(BaseRenderer):
    def render(self, shapes):
        # Implementation
        pass
```

## Testing Strategy

### Unit Tests
- Individual shape operations
- Boolean operations
- Transformations
- I/O operations

### Integration Tests
- Multi-step workflows
- Assembly creation
- Reactive updates
- Visualization rendering

### Performance Tests
- Large model handling
- Memory usage
- Rendering speed
- Cache effectiveness

### Example Tests
```python
def test_box_creation():
    box = primitives.box(10, 10, 10)
    assert box.volume == 1000
    assert len(box.faces()) == 6

def test_boolean_union():
    box1 = primitives.box(10, 10, 10)
    box2 = primitives.box(10, 10, 10).translate(x=5)
    union = box1 + box2
    assert union.volume == 1500

def test_reactive_update():
    param = ReactiveParameter(value=10)
    box = primitives.box(param.value, 10, 10)
    initial_volume = box.volume
    
    param.value = 20
    updated_box = primitives.box(param.value, 10, 10)
    assert updated_box.volume == 2 * initial_volume
```

## Security Considerations

### 1. Input Validation
- Validate all user inputs
- Sanitize file paths
- Check geometric constraints

### 2. Resource Limits
- Maximum model size
- Maximum computation time
- Memory limits

### 3. Safe File Operations
- Validate file formats
- Sandbox file I/O
- Prevent path traversal

## Deployment

### Package Distribution
- PyPI package
- Conda package
- Docker image

### Documentation
- API reference (auto-generated)
- User guide with examples
- Architecture documentation
- Tutorial notebooks

### Version Management
- Semantic versioning
- Changelog
- Migration guides

## Future Architecture Enhancements

### 1. Cloud Integration
- Server-side rendering
- Distributed computation
- Cloud storage for models

### 2. Collaboration Features
- Multi-user editing
- Version control for models
- Shared parameter spaces

### 3. Advanced Analysis
- Finite Element Analysis (FEA)
- Computational Fluid Dynamics (CFD)
- Topology optimization

### 4. Manufacturing Integration
- G-code generation
- CNC toolpath planning
- 3D printing optimization

### 5. AI/ML Integration
- Shape recommendation
- Parameter optimization
- Generative design

## Conclusion

The marimocad architecture is designed to provide a robust, scalable, and user-friendly platform for CAD modeling in Marimo notebooks. The layered architecture ensures separation of concerns while maintaining flexibility for future extensions. The reactive core seamlessly integrates with Marimo's reactive programming model, providing an intuitive and powerful user experience.
