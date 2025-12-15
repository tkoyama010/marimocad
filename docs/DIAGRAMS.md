# marimocad Visual Architecture Diagrams

## System Architecture Overview

```
╔══════════════════════════════════════════════════════════════════════════╗
║                          MARIMO NOTEBOOK LAYER                           ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  User Interface Components                                         │  ║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │  ║
║  │  │ Sliders  │ │  Inputs  │ │Dropdowns │ │  Tables  │             │  ║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │  ║
║  │                                                                     │  ║
║  │  Reactive Cell Execution (Auto-updates on parameter changes)      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │ Python API calls
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                          MARIMOCAD API LAYER                             ║
║  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      ║
║  │ Primitives  │ │  Boolean    │ │   Transform │ │  Modifier   │      ║
║  │   Module    │ │  Operations │ │    Module   │ │   Module    │      ║
║  │             │ │             │ │             │ │             │      ║
║  │ • box()     │ │ • union()   │ │ • translate │ │ • fillet()  │      ║
║  │ • sphere()  │ │ • subtract()│ │ • rotate()  │ │ • chamfer() │      ║
║  │ • cylinder()│ │ • intersect │ │ • scale()   │ │ • shell()   │      ║
║  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      ║
║                                                                          ║
║  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      ║
║  │   Sketch    │ │  Assembly   │ │    I/O      │ │ Measurement │      ║
║  │   Module    │ │   Module    │ │   Module    │ │   Module    │      ║
║  │             │ │             │ │             │ │             │      ║
║  │ • circles   │ │ • add_part()│ │ • import()  │ │ • volume    │      ║
║  │ • rectangles│ │ • constrain │ │ • export()  │ │ • area      │      ║
║  │ • extrude() │ │ • save()    │ │ • formats   │ │ • mass_prop │      ║
║  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      ║
╚══════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │ Shape operations
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                          REACTIVE CORE LAYER                             ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Shape Dependency Graph (DAG)                                      │  ║
║  │                                                                     │  ║
║  │     ┌────────┐                                                     │  ║
║  │     │ Param1 │──────┐                                             │  ║
║  │     └────────┘      │                                             │  ║
║  │                     ▼                                             │  ║
║  │     ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │  ║
║  │     │ Param2 │─▶│ Shape A  │─▶│ Shape B  │─▶│ Shape C  │        │  ║
║  │     └────────┘  └──────────┘  └──────────┘  └──────────┘        │  ║
║  │                                                                     │  ║
║  │  Features:                                                         │  ║
║  │  • Dependency tracking     • Lazy evaluation                      │  ║
║  │  • Auto-invalidation       • Result caching                       │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Parameter Manager                                                 │  ║
║  │  • Observable parameters                                           │  ║
║  │  • Change notifications                                            │  ║
║  │  • Validation & constraints                                        │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │ Geometry requests
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                        GEOMETRY ENGINE LAYER                             ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Shape Class Hierarchy                                             │  ║
║  │                                                                     │  ║
║  │                    ┌──────────┐                                    │  ║
║  │                    │  Shape   │  (Base Class)                      │  ║
║  │                    └──────────┘                                    │  ║
║  │                         │                                          │  ║
║  │          ┌──────────────┴──────────────┐                          │  ║
║  │          ▼                              ▼                          │  ║
║  │     ┌──────────┐                  ┌──────────┐                    │  ║
║  │     │ Shape2D  │                  │ Shape3D  │                    │  ║
║  │     └──────────┘                  └──────────┘                    │  ║
║  │          │                              │                          │  ║
║  │     ┌────┴────┐              ┌─────────┼─────────┐               │  ║
║  │     ▼         ▼              ▼         ▼         ▼               │  ║
║  │  Circle  Rectangle        Box     Sphere   Cylinder              │  ║
║  │                                                                     │  ║
║  │  Features:                                                         │  ║
║  │  • Immutable objects       • Operation history                    │  ║
║  │  • BREP topology           • Provenance tracking                  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Topological Operations                                            │  ║
║  │  • Face/Edge/Vertex selection   • Topology queries                │  ║
║  │  • Filtering and iteration      • Geometric properties            │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │ Visualization requests
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                         VISUALIZATION LAYER                              ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Mesh Generation Pipeline                                          │  ║
║  │                                                                     │  ║
║  │  BREP Surface ──▶ Tessellation ──▶ Triangulation ──▶ WebGL Mesh  │  ║
║  │                                                                     │  ║
║  │  Features:                                                         │  ║
║  │  • Adaptive refinement based on curvature                         │  ║
║  │  • Multiple LOD (Level of Detail) levels                          │  ║
║  │  • Normal and UV coordinate generation                            │  ║
║  │  • Progressive mesh streaming                                      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Rendering Backends                                                │  ║
║  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                     │  ║
║  │  │ Three.js  │  │Babylon.js │  │   WebGL   │                     │  ║
║  │  │(Primary)  │  │(Optional) │  │  (Direct) │                     │  ║
║  │  └───────────┘  └───────────┘  └───────────┘                     │  ║
║  │                                                                     │  ║
║  │  Features:                                                         │  ║
║  │  • Hardware-accelerated rendering                                 │  ║
║  │  • Interactive camera controls                                     │  ║
║  │  • Material and lighting                                           │  ║
║  │  • Export to image formats                                         │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │ Geometric operations
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                      CAD KERNEL LAYER (OpenCASCADE)                      ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Core Geometric Services                                           │  ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  ║
║  │  │  Boolean    │  │   Surface   │  │   Import/   │               │  ║
║  │  │ Operations  │  │  Operations │  │   Export    │               │  ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘               │  ║
║  │                                                                     │  ║
║  │  Features:                                                         │  ║
║  │  • Union, Difference, Intersection                                 │  ║
║  │  • NURBS surfaces and curves                                       │  ║
║  │  • Filleting, chamfering, offsetting                               │  ║
║  │  • STEP, IGES, STL file formats                                    │  ║
║  │  • High-precision BREP modeling                                    │  ║
║  │  • Industry-proven reliability                                     │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
```

## Data Flow Diagram: Creating and Visualizing a Shape

```
User Code                    API Layer              Reactive Core        Geometry Engine      Visualization
    │                           │                         │                    │                   │
    │  box = primitives.box()   │                         │                    │                   │
    ├──────────────────────────▶│                         │                    │                   │
    │                           │ Create Shape3D object   │                    │                   │
    │                           ├────────────────────────▶│                    │                   │
    │                           │                         │ Register in graph  │                   │
    │                           │                         │ (no evaluation)    │                   │
    │                           │◀────────────────────────┤                    │                   │
    │◀──────────────────────────┤                         │                    │                   │
    │                           │                         │                    │                   │
    │  visualize(box)           │                         │                    │                   │
    ├──────────────────────────▶│                         │                    │                   │
    │                           │ Request geometry data   │                    │                   │
    │                           ├────────────────────────▶│                    │                   │
    │                           │                         │ Evaluate shape     │                   │
    │                           │                         ├───────────────────▶│                   │
    │                           │                         │                    │ Call OCC kernel   │
    │                           │                         │                    │ Get BREP data     │
    │                           │                         │◀───────────────────┤                   │
    │                           │                         │ Cache result       │                   │
    │                           │◀────────────────────────┤                    │                   │
    │                           │ Pass geometry           │                    │                   │
    │                           ├───────────────────────────────────────────────────────────────▶│
    │                           │                         │                    │  Tessellate       │
    │                           │                         │                    │  Generate mesh    │
    │                           │                         │                    │  Render in viewer │
    │                           │◀───────────────────────────────────────────────────────────────┤
    │◀──────────────────────────┤                         │                    │                   │
    │  Display viewer           │                         │                    │                   │
    │                           │                         │                    │                   │
```

## Data Flow Diagram: Reactive Parameter Update

```
User Action            Marimo Layer        Reactive Core       API Layer      Visualization
    │                      │                    │                  │                │
    │ Slider moved         │                    │                  │                │
    │ (radius changed)     │                    │                  │                │
    ├─────────────────────▶│                    │                  │                │
    │                      │ Detect change      │                  │                │
    │                      │ Trigger re-exec    │                  │                │
    │                      ├───────────────────▶│                  │                │
    │                      │                    │ Invalidate cache │                │
    │                      │                    │ for dependents   │                │
    │                      │                    ├─────────────────▶│                │
    │                      │                    │                  │ Create new     │
    │                      │                    │                  │ shape with     │
    │                      │                    │                  │ new parameter  │
    │                      │                    │◀─────────────────┤                │
    │                      │◀───────────────────┤                  │                │
    │                      │ Pass to visualizer │                  │                │
    │                      ├───────────────────────────────────────────────────────▶│
    │                      │                    │                  │  Re-render     │
    │                      │                    │                  │  with cached   │
    │                      │                    │                  │  results where │
    │                      │                    │                  │  possible      │
    │◀─────────────────────┤                    │                  │                │
    │ Updated display      │                    │                  │                │
    │                      │                    │                  │                │
```

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         User Space                                  │
│                                                                     │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐       │
│  │   Marimo    │      │  User Code  │      │  3D Viewer  │       │
│  │  Controls   │─────▶│  (Notebook  │─────▶│  (Browser)  │       │
│  │  (Sliders)  │      │    Cells)   │      │             │       │
│  └─────────────┘      └─────────────┘      └─────────────┘       │
│         │                     │                     │              │
└─────────┼─────────────────────┼─────────────────────┼──────────────┘
          │                     │                     │
          │                     │                     │
┌─────────┼─────────────────────┼─────────────────────┼──────────────┐
│         ▼                     ▼                     ▼              │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │              marimocad Library                           │      │
│  │                                                          │      │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │      │
│  │  │   Shape    │  │  Reactive  │  │    Mesh    │       │      │
│  │  │ Operations │◀─│   Graph    │─▶│  Generator │       │      │
│  │  └────────────┘  └────────────┘  └────────────┘       │      │
│  │         │              │                  │             │      │
│  └─────────┼──────────────┼──────────────────┼─────────────┘      │
│            │              │                  │                    │
└────────────┼──────────────┼──────────────────┼────────────────────┘
             │              │                  │
             │              │                  │
┌────────────┼──────────────┼──────────────────┼────────────────────┐
│            ▼              ▼                  ▼                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │           External Dependencies                          │     │
│  │                                                          │     │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │     │
│  │  │ OpenCASCADE│  │  Three.js  │  │   NumPy    │       │     │
│  │  │    (OCP)   │  │   (WebGL)  │  │  (Arrays)  │       │     │
│  │  └────────────┘  └────────────┘  └────────────┘       │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Class Diagram: Core Shape Classes

```
                    ┌─────────────────────────┐
                    │       Shape             │
                    │    (Abstract Base)      │
                    ├─────────────────────────┤
                    │ - _geometry             │
                    │ - _params               │
                    │ - _history              │
                    │ - _cached_data          │
                    ├─────────────────────────┤
                    │ + volume                │
                    │ + surface_area          │
                    │ + center_of_mass        │
                    │ + bounding_box          │
                    │ + translate()           │
                    │ + rotate()              │
                    │ + scale()               │
                    │ + union()               │
                    │ + subtract()            │
                    │ + intersect()           │
                    │ + __add__()             │
                    │ + __sub__()             │
                    │ + __and__()             │
                    └─────────────────────────┘
                              △
                              │
                ┌─────────────┴─────────────┐
                │                           │
                │                           │
    ┌───────────────────────┐   ┌───────────────────────┐
    │      Shape2D          │   │      Shape3D          │
    ├───────────────────────┤   ├───────────────────────┤
    │ + area                │   │ + volume              │
    │ + perimeter           │   │ + faces()             │
    │ + extrude()           │   │ + edges()             │
    │ + revolve()           │   │ + vertices()          │
    │ + offset()            │   │ + fillet()            │
    └───────────────────────┘   │ + chamfer()           │
                │               │ + shell()             │
                │               │ + offset()            │
                │               └───────────────────────┘
                │                           △
    ┌───────────┴───────────┐               │
    │                       │               │
┌───────────┐     ┌─────────────┐  ┌────────┴──────┐
│  Circle   │     │  Rectangle  │  │      Box      │
├───────────┤     ├─────────────┤  ├───────────────┤
│ + radius  │     │ + width     │  │ + width       │
└───────────┘     │ + height    │  │ + height      │
                  └─────────────┘  │ + depth       │
                                   └───────────────┘
        ┌──────────────────────────────┴──────┬──────────────┐
        │                                     │              │
┌───────────────┐                   ┌─────────────┐  ┌──────────────┐
│    Sphere     │                   │  Cylinder   │  │     Cone     │
├───────────────┤                   ├─────────────┤  ├──────────────┤
│ + radius      │                   │ + radius    │  │ + radius     │
└───────────────┘                   │ + height    │  │ + height     │
                                    └─────────────┘  └──────────────┘
```

## Sequence Diagram: Boolean Operation

```
User    API      ReactiveCore  GeometryEngine    OCC Kernel    Cache
 │       │            │              │                │          │
 │ box1+box2          │              │                │          │
 ├──────▶│            │              │                │          │
 │       │ create union shape        │                │          │
 │       ├───────────▶│              │                │          │
 │       │            │ register dependency           │          │
 │       │            │ (lazy, no eval)               │          │
 │       │◀───────────┤              │                │          │
 │◀──────┤            │              │                │          │
 │       │            │              │                │          │
 │ visualize()        │              │                │          │
 ├──────▶│            │              │                │          │
 │       │ need geometry             │                │          │
 │       ├───────────▶│              │                │          │
 │       │            │ check cache  │                │          │
 │       │            ├──────────────────────────────▶│          │
 │       │            │              │                │ miss     │
 │       │            │◀──────────────────────────────┤          │
 │       │            │              │                │          │
 │       │            │ evaluate     │                │          │
 │       │            ├─────────────▶│                │          │
 │       │            │              │ BRepAlgoAPI_Fuse          │
 │       │            │              ├───────────────▶│          │
 │       │            │              │                │          │
 │       │            │              │ BREP result    │          │
 │       │            │              │◀───────────────┤          │
 │       │            │ geometry     │                │          │
 │       │            │◀─────────────┤                │          │
 │       │            │ store in cache                │          │
 │       │            ├──────────────────────────────▶│          │
 │       │ geometry   │              │                │          │
 │       │◀───────────┤              │                │          │
 │◀──────┤            │              │                │          │
 │       │            │              │                │          │
```

## Legend

```
╔═══╗  Major system boundary
║   ║
╚═══╝

┌───┐  Component or module
│   │
└───┘

───▶  Data flow or call
◀───  Return or response

 △    Inheritance (is-a)
 │
 
 ◇    Composition (has-a)
 │
```
