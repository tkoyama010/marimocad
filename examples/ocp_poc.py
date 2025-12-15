"""OCP (OpenCascade Python) Proof of Concept for Marimo Integration

This example demonstrates how direct OCP usage would work with Marimo.
OCP is NOT recommended as a user-facing API due to its complexity,
but it's the foundation that both CadQuery and Build123d are built on.

This is included for completeness to show why high-level wrappers are preferred.
"""

import marimo


__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __():
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
    from OCP.BRepPrimAPI import (
        BRepPrimAPI_MakeBox,
        BRepPrimAPI_MakeCylinder,
        BRepPrimAPI_MakeSphere,
    )
    from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
    from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
    from OCP.StlAPI import StlAPI_Writer
    from OCP.TopAbs import TopAbs_EDGE
    from OCP.TopExp import TopExp_Explorer

    return (
        BRepAlgoAPI_Cut,
        BRepAlgoAPI_Fuse,
        BRepFilletAPI_MakeFillet,
        BRepPrimAPI_MakeBox,
        BRepPrimAPI_MakeCylinder,
        BRepPrimAPI_MakeSphere,
        STEPControl_AsIs,
        STEPControl_Writer,
        StlAPI_Writer,
        TopAbs_EDGE,
        TopExp_Explorer,
        gp_Ax2,
        gp_Dir,
        gp_Pnt,
        gp_Vec,
    )


@app.cell
def __(mo):
    mo.md("""
    # OCP (Direct OpenCascade) Demo

    This demonstrates direct OCP usage - **not recommended** for marimocad!

    This is shown for educational purposes to understand:
    1. Why CadQuery and Build123d exist
    2. The complexity of low-level CAD operations
    3. What's happening "under the hood"
    """)


@app.cell
def __(mo):
    mo.md("""
    ## Example 1: Creating a Simple Box

    Compare the code complexity below with the high-level alternatives:

    **CadQuery:** `cq.Workplane("XY").box(10, 10, 10)`
    **Build123d:** `Box(10, 10, 10)`
    **OCP:** (see below)
    """)


@app.cell
def __(BRepPrimAPI_MakeBox):
    # OCP: Creating a simple box
    box_maker = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0)
    box_shape = box_maker.Shape()

    "Box created (shape object, not visualizable directly)"
    return box_maker, box_shape


@app.cell
def __(mo):
    mo.md("""
    ## Example 2: Boolean Operation (Box with Hole)

    **CadQuery:**
    ```python
    result = cq.Workplane("XY").box(20, 20, 5).faces(">Z").workplane().hole(5)
    ```

    **Build123d:**
    ```python
    with BuildPart() as p:
        Box(20, 20, 5)
        with Locations(p.faces().sort_by(Axis.Z)[-1]):
            Hole(2.5)
    ```

    **OCP:** (see below)
    """)


@app.cell
def __(
    BRepAlgoAPI_Cut,
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder,
    gp_Ax2,
    gp_Dir,
    gp_Pnt,
):
    # OCP: Box with hole (much more verbose!)
    # Step 1: Create box
    ocp_box_maker = BRepPrimAPI_MakeBox(20.0, 20.0, 5.0)
    ocp_box = ocp_box_maker.Shape()

    # Step 2: Create cylinder for hole
    # Need to define axis and position
    axis = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    cylinder_maker = BRepPrimAPI_MakeCylinder(axis, 2.5, 5.0)
    cylinder = cylinder_maker.Shape()

    # Step 3: Perform boolean cut
    cut_operation = BRepAlgoAPI_Cut(ocp_box, cylinder)
    cut_operation.Build()

    # Step 4: Check if operation succeeded
    if cut_operation.IsDone():
        box_with_hole = cut_operation.Shape()
        result_msg = "Boolean operation successful"
    else:
        result_msg = "Boolean operation failed"

    result_msg
    return (
        axis,
        box_with_hole,
        cut_operation,
        cylinder,
        cylinder_maker,
        ocp_box,
        ocp_box_maker,
        result_msg,
    )


@app.cell
def __(mo):
    mo.md("""
    ## Example 3: Export

    Even export operations are more complex with OCP:
    """)


@app.cell
def __(STEPControl_AsIs, STEPControl_Writer, box_shape):
    # OCP: Export to STEP
    def export_step_ocp(shape, filename):
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        status = writer.Write(filename)
        return "Success" if status == 1 else "Failed"

    # Example (commented to avoid file creation):
    # export_step_ocp(box_shape, "/tmp/ocp_box.step")

    "Export function defined (requires explicit calls)"
    return (export_step_ocp,)


@app.cell
def __(mo):
    mo.md("""
    ## Code Comparison Summary

    ### Creating a Box with Hole

    | Library | Lines of Code | Readability |
    |---------|---------------|-------------|
    | **CadQuery** | 1 line | ⭐⭐⭐⭐⭐ Excellent |
    | **Build123d** | 4 lines | ⭐⭐⭐⭐⭐ Excellent |
    | **OCP** | 15+ lines | ⭐⭐ Poor |

    ### API Characteristics

    | Feature | CadQuery | Build123d | OCP |
    |---------|----------|-----------|-----|
    | **Pythonic** | ✅ Yes | ✅ Yes | ❌ No |
    | **Type Hints** | ⚠️ Partial | ✅ Yes | ❌ No |
    | **Error Messages** | ✅ Clear | ✅ Clear | ❌ Cryptic |
    | **Documentation** | ✅ Excellent | ✅ Good | ⚠️ C++ docs |
    | **Learning Curve** | ✅ Easy | ✅ Easy | ❌ Steep |
    | **Code Verbosity** | ✅ Concise | ✅ Concise | ❌ Verbose |

    """)


@app.cell
def __(mo):
    mo.md("""
    ## Why Not Use OCP Directly?

    ### Cons of Direct OCP Usage:

    1. **Verbose Code**: 10-20x more code for same operations
    2. **Not Pythonic**: Exposes C++ API directly
    3. **Poor Error Messages**: OpenCascade exceptions are cryptic
    4. **Steep Learning Curve**: Requires OpenCascade knowledge
    5. **Manual Memory Management**: Need to handle topology carefully
    6. **No High-Level Concepts**: Missing workplanes, selectors, etc.
    7. **Hard to Debug**: Complex object hierarchies
    8. **No Parametric Helpers**: Must build from scratch

    ### When OCP Direct Usage Makes Sense:

    1. **Performance Critical**: When every microsecond counts
    2. **Custom Algorithms**: Implementing new CAD algorithms
    3. **Advanced Features**: Features not exposed by wrappers
    4. **Library Development**: Building new high-level wrappers

    ### For marimocad:

    ❌ **Do NOT use OCP directly** for user-facing API
    ✅ **Use Build123d or CadQuery** as high-level wrappers
    ℹ️ **OCP is the foundation** both libraries use internally

    """)


@app.cell
def __(mo):
    mo.md("""
    ## Architecture Recommendation

    ```
    ┌─────────────────────────────────────┐
    │         marimocad API               │  <- User-facing API
    │  (Simple, Pythonic, Marimo-ready)   │
    └──────────────┬──────────────────────┘
                   │
    ┌──────────────┴──────────────────────┐
    │                                     │
    ┌──────────────┴──────┐  ┌───────────┴─────────┐
    │    Build123d        │  │     CadQuery        │  <- High-level CAD
    │   (Primary)         │  │   (Secondary)       │
    └──────────────┬──────┘  └───────────┬─────────┘
                   │                     │
                   └──────────┬──────────┘
                              │
                   ┌──────────┴──────────┐
                   │        OCP          │  <- Low-level engine
                   │  (OpenCascade)      │
                   └─────────────────────┘
    ```

    **Benefits:**
    - Users get simple, intuitive API
    - Power users can drop down to Build123d/CadQuery
    - Experts can access OCP when needed
    - Maximum flexibility with good defaults
    """)


@app.cell
def __(mo):
    mo.md("""
    ## Conclusion

    This proof of concept demonstrates why direct OCP usage is not suitable
    for marimocad's user-facing API:

    1. **Too Complex**: Requires deep CAD knowledge
    2. **Too Verbose**: 10-20x more code
    3. **Not User-Friendly**: Poor Python integration
    4. **Hard to Learn**: Steep learning curve

    **Recommendation**: Use Build123d as primary backend, which provides:
    - Clean, Pythonic API
    - Full access to OCP power when needed
    - Great Marimo integration
    - Modern Python features

    CadQuery is excellent as a secondary option for users who prefer
    its fluent API style.
    """)


if __name__ == "__main__":
    app.run()
