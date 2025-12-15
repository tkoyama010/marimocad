# marimocad Documentation

This directory contains comprehensive documentation for the marimocad project.

## Documents

### [API_SPECIFICATION.md](./API_SPECIFICATION.md)
Complete API specification including:
- Core geometry creation functions (primitives, sketches, advanced surfaces)
- Transformation operations
- Boolean operations
- Modification operations (filleting, chamfering, shelling)
- Measurement and query functions
- Marimo integration patterns
- 3D visualization components
- Data structures and class hierarchies
- File I/O interfaces (STEP, STL, IGES, OBJ, GLTF)
- Type hints and error handling

### [ARCHITECTURE.md](./ARCHITECTURE.md)
System architecture documentation including:
- Layered architecture diagram
- Component details for each layer
- Data flow patterns
- Design patterns used
- Technology stack
- Performance optimization strategies
- Testing strategy
- Security considerations
- Deployment information
- Future architecture enhancements

### [DESIGN_DECISIONS.md](./DESIGN_DECISIONS.md)
Rationale for key design decisions including:
- Immutable shape objects
- Fluent interface and method chaining
- Context managers for complex construction
- Operator overloading for boolean operations
- Lazy evaluation with caching
- Reactive parameter system
- Type hints
- OpenCASCADE as geometry kernel
- Three.js for visualization
- Progressive rendering
- Selector syntax for topology
- Assembly as first-class concept
- File format support
- Error handling strategy
- Component-based modeling

### [examples.py](./examples.py)
Comprehensive example code demonstrating:
1. Basic primitive creation and visualization
2. Boolean operations (union, difference, intersection)
3. Transformations (translate, rotate, scale, mirror)
4. Reactive parameters with Marimo UI controls
5. Sketch-based modeling
6. Parametric component classes
7. Assembly creation and management
8. Advanced surface modeling with loft
9. Sweep operations
10. Complex parts with modifications
11. Measurements and queries
12. File import/export
13. Interactive design iteration
14. Pattern creation
15. Complex assemblies with constraints

### [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
Executive summary covering:
- Project overview and problem statement
- Key features and capabilities
- Architecture summary
- Design principles
- Technology stack
- Implementation status
- Use cases and applications
- Comparison with alternatives
- Performance considerations
- Future enhancements
- Success metrics

### [DIAGRAMS.md](./DIAGRAMS.md)
Visual architecture diagrams including:
- System architecture overview (multi-layer diagram)
- Data flow diagrams (shape creation and reactive updates)
- Component interaction diagram
- Class hierarchy diagram
- Sequence diagrams for operations
- Detailed ASCII art representations

## Quick Start

For new users, we recommend reading the documents in this order:

1. **API_SPECIFICATION.md** - Understand what the library can do
2. **PROJECT_SUMMARY.md** - Get a high-level overview
3. **examples.py** - See practical usage examples
4. **ARCHITECTURE.md** - Understand how it works internally
5. **DIAGRAMS.md** - Visualize the system architecture
6. **DESIGN_DECISIONS.md** - Learn why design choices were made

## Contributing

When contributing to marimocad, please:
- Keep documentation in sync with code changes
- Add examples for new features
- Update design decisions when making architectural changes
- Maintain the clear, educational tone of existing docs

## Version

Current documentation version: v0.1.0 (Initial Design)

## License

Documentation is licensed under the same terms as the marimocad project.
