"""Marimo integration for marimocad.

This module provides Marimo-specific components for interactive CAD modeling,
including the viewer component and parametric model helpers.
"""

from __future__ import annotations

import warnings

from typing import Any, Callable

from marimocad.viewer import create_threejs_viewer, geometry_to_mesh_data


def viewer(
    geom: Any | list[Any] | None = None,
    width: int = 800,
    height: int = 600,
    background_color: str = "#f0f0f0",
    camera_position: tuple[float, float, float] = (50, 50, 50),
) -> Any:
    """Create an interactive 3D viewer for Marimo notebooks.

    This function creates a Three.js-based 3D viewer that displays CAD geometries
    with interactive camera controls (rotate, pan, zoom), lighting, and selection.

    Args:
        geom: Geometry or list of geometries to display
        width: Viewer width in pixels
        height: Viewer height in pixels
        background_color: Background color in hex format
        camera_position: Initial camera position (x, y, z)

    Returns:
        Marimo HTML component with 3D viewer

    Example:
        >>> import marimo as mo
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> mc.viewer(box)

    Features:
        - Interactive camera controls (orbit, pan, zoom)
        - Multiple geometries in one view
        - Geometry selection and highlighting
        - Wireframe toggle
        - Grid and axes helpers
        - Automatic camera positioning
    """
    try:
        import marimo as mo
    except ImportError as e:
        msg = "marimo is required for the viewer. Install with: pip install marimo"
        raise ImportError(msg) from e

    if geom is None:
        # Return empty viewer
        html = create_threejs_viewer([], width, height, background_color, camera_position)
        return mo.Html(html)

    # Handle single geometry or list
    geometries = geom if isinstance(geom, list) else [geom]

    # Convert geometries to mesh data
    mesh_data_list = []
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]

    for i, geometry in enumerate(geometries):
        try:
            mesh_data = geometry_to_mesh_data(geometry)
            # Assign different colors to different geometries
            mesh_data["color"] = colors[i % len(colors)]
            mesh_data_list.append(mesh_data)
        except (ValueError, AttributeError, ImportError) as e:
            # Skip geometries that can't be converted
            warnings.warn(f"Could not convert geometry {i}: {e}", stacklevel=2)
            continue

    if not mesh_data_list:
        # No valid geometries, return empty viewer
        html = create_threejs_viewer([], width, height, background_color, camera_position)
        return mo.Html(html)

    # Create and return viewer
    html = create_threejs_viewer(
        mesh_data_list,
        width,
        height,
        background_color,
        camera_position,
    )
    return mo.Html(html)


class GeometryCard:
    """Marimo UI card displaying geometry properties.

    This class creates an informational card that displays properties of a geometry
    object, such as number of faces, edges, vertices, volume, and surface area.

    Example:
        >>> import marimocad as mc
        >>> box = mc.box(10, 10, 10)
        >>> card = mc.GeometryCard(box)
        >>> card.render()
    """

    def __init__(self, geom: Any) -> None:
        """Create a geometry info card.

        Args:
            geom: Geometry to display info for
        """
        self.geom = geom
        self._properties = self._extract_properties()

    def _extract_properties(self) -> dict[str, Any]:
        """Extract properties from the geometry.

        Returns:
            Dictionary of property names and values
        """
        properties = {}

        # Try to extract common properties
        try:
            # Build123d
            if hasattr(self.geom, "faces"):
                properties["Faces"] = len(self.geom.faces())
            if hasattr(self.geom, "edges"):
                properties["Edges"] = len(self.geom.edges())
            if hasattr(self.geom, "vertices"):
                properties["Vertices"] = len(self.geom.vertices())
            if hasattr(self.geom, "volume"):
                vol = self.geom.volume
                properties["Volume"] = f"{vol:.2f}"
            if hasattr(self.geom, "area"):
                area = self.geom.area
                properties["Surface Area"] = f"{area:.2f}"

            # Bounding box
            if hasattr(self.geom, "bounding_box"):
                bbox = self.geom.bounding_box()
                if bbox:
                    properties["Bounding Box"] = (
                        f"({bbox.min.X:.1f}, {bbox.min.Y:.1f}, {bbox.min.Z:.1f}) to "
                        f"({bbox.max.X:.1f}, {bbox.max.Y:.1f}, {bbox.max.Z:.1f})"
                    )
        except (AttributeError, TypeError):
            # If extraction fails, just show type
            properties["Type"] = str(type(self.geom).__name__)

        return properties

    def render(self) -> Any:
        """Render the geometry info card.

        Returns:
            Marimo HTML component with the info card
        """
        try:
            import marimo as mo
        except ImportError as e:
            msg = "marimo is required. Install with: pip install marimo"
            raise ImportError(msg) from e

        # Create markdown table
        rows = []
        for key, value in self._properties.items():
            rows.append(f"| **{key}** | {value} |")

        table = "\n".join(rows)
        markdown = f"""
## Geometry Properties

| Property | Value |
|----------|-------|
{table}
"""
        return mo.md(markdown)


def parametric_model(
    func: Callable[..., Any],
    params: dict[str, Any],
    width: int = 800,
    height: int = 600,
) -> Any:
    """Create a reactive parametric model viewer.

    This function combines a model creation function with UI parameters to create
    a reactive 3D viewer that updates automatically when parameters change.

    Args:
        func: Function that creates geometry from parameters
        params: Dictionary of Marimo UI elements (sliders, inputs, etc.)
        width: Viewer width in pixels
        height: Viewer height in pixels

    Returns:
        Interactive parametric model viewer with controls

    Example:
        >>> import marimo as mo
        >>> import marimocad as mc
        >>>
        >>> def create_box(length, width, height):
        ...     return mc.box(length, width, height)
        >>>
        >>> params = {
        ...     "length": mo.ui.slider(1, 20, value=10),
        ...     "width": mo.ui.slider(1, 20, value=10),
        ...     "height": mo.ui.slider(1, 20, value=10),
        ... }
        >>>
        >>> mc.parametric_model(create_box, params)
    """
    try:
        import marimo as mo
    except ImportError as e:
        msg = "marimo is required. Install with: pip install marimo"
        raise ImportError(msg) from e

    # Extract parameter values
    param_values = {name: ui_element.value for name, ui_element in params.items()}

    # Create geometry
    try:
        geometry = func(**param_values)
    except Exception as e:
        error_html = f"""
        <div style="padding: 20px; background: #fee; border: 1px solid #fcc; border-radius: 5px;">
            <h3>Error creating geometry</h3>
            <p>{e!s}</p>
        </div>
        """
        return mo.Html(error_html)

    # Create viewer
    viewer_component = viewer(geometry, width=width, height=height)

    # Create parameter controls
    controls = mo.vstack(list(params.values()))

    # Combine controls and viewer
    return mo.hstack([controls, viewer_component])
