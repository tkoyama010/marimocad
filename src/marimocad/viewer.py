"""3D Viewer component for Marimo notebooks.

This module provides interactive 3D visualization for CAD geometries using Three.js.
The viewer supports camera controls, lighting, materials, and geometry selection.
"""

import json

from typing import Any


def create_threejs_viewer(
    geometries: list[dict[str, Any]],
    width: int = 800,
    height: int = 600,
    background_color: str = "#f0f0f0",
    camera_position: tuple[float, float, float] = (50, 50, 50),
) -> str:
    """Create a Three.js-based 3D viewer HTML component.

    Args:
        geometries: List of geometry data dictionaries containing vertices and faces
        width: Viewer width in pixels
        height: Viewer height in pixels
        background_color: Background color in hex format
        camera_position: Initial camera position (x, y, z)

    Returns:
        HTML string containing the complete Three.js viewer

    Example:
        >>> geometry = {"vertices": [...], "faces": [...], "color": "#ff0000"}
        >>> html = create_threejs_viewer([geometry])
    """
    geometries_json = json.dumps(geometries)
    camera_pos_json = json.dumps(list(camera_position))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; }}
            #viewer-container {{ width: {width}px; height: {height}px; }}
            #controls {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 12px;
            }}
            .control-row {{
                margin: 5px 0;
            }}
            label {{
                display: inline-block;
                width: 100px;
            }}
        </style>
    </head>
    <body>
        <div id="viewer-container"></div>
        <div id="controls">
            <div class="control-row">
                <strong>Camera Controls</strong>
            </div>
            <div class="control-row">
                Left click: Rotate
            </div>
            <div class="control-row">
                Right click: Pan
            </div>
            <div class="control-row">
                Scroll: Zoom
            </div>
            <div class="control-row">
                <label>Wireframe:</label>
                <input type="checkbox" id="wireframe-toggle">
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
        <script>
            // Scene setup
            const container = document.getElementById('viewer-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color('{background_color}');

            // Camera setup
            const camera = new THREE.PerspectiveCamera(
                45,
                {width} / {height},
                0.1,
                10000
            );
            camera.position.set(...{camera_pos_json});

            // Renderer setup
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize({width}, {height});
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            // Orbit controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);

            const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight1.position.set(1, 1, 1);
            scene.add(directionalLight1);

            const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
            directionalLight2.position.set(-1, -1, -1);
            scene.add(directionalLight2);

            // Grid helper
            const gridHelper = new THREE.GridHelper(100, 20);
            scene.add(gridHelper);

            // Axes helper
            const axesHelper = new THREE.AxesHelper(20);
            scene.add(axesHelper);

            // Load geometries
            const geometries = {geometries_json};
            const meshes = [];

            geometries.forEach((geomData, index) => {{
                const geometry = new THREE.BufferGeometry();

                // Set vertices
                const vertices = new Float32Array(geomData.vertices.flat());
                geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

                // Set faces (indices)
                if (geomData.faces) {{
                    const indices = new Uint32Array(geomData.faces.flat());
                    geometry.setIndex(new THREE.BufferAttribute(indices, 1));
                }}

                // Compute normals for proper lighting
                geometry.computeVertexNormals();

                // Material
                const color = geomData.color || '#3498db';
                const material = new THREE.MeshPhongMaterial({{
                    color: color,
                    shininess: 30,
                    flatShading: false,
                    side: THREE.DoubleSide
                }});

                const mesh = new THREE.Mesh(geometry, material);
                mesh.userData.originalColor = color;
                mesh.userData.index = index;
                scene.add(mesh);
                meshes.push(mesh);
            }});

            // Wireframe toggle
            document.getElementById('wireframe-toggle').addEventListener('change', (e) => {{
                meshes.forEach(mesh => {{
                    mesh.material.wireframe = e.target.checked;
                }});
            }});

            // Mouse interaction for selection
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            let selectedMesh = null;

            container.addEventListener('click', (event) => {{
                const rect = container.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(meshes);

                // Deselect previous
                if (selectedMesh) {{
                    selectedMesh.material.color.setStyle(
                        selectedMesh.userData.originalColor
                    );
                    selectedMesh.material.emissive.setHex(0x000000);
                }}

                // Select new
                if (intersects.length > 0) {{
                    selectedMesh = intersects[0].object;
                    selectedMesh.material.emissive.setHex(0x555555);
                }} else {{
                    selectedMesh = null;
                }}
            }});

            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            // Auto-fit camera to view all objects
            if (meshes.length > 0) {{
                const box = new THREE.Box3();
                meshes.forEach(mesh => {{
                    box.expandByObject(mesh);
                }});

                const center = box.getCenter(new THREE.Vector3());
                const size = box.getSize(new THREE.Vector3());
                const maxDim = Math.max(size.x, size.y, size.z);
                const fov = camera.fov * (Math.PI / 180);
                let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
                cameraZ *= 1.5; // Add some padding

                camera.position.set(center.x + cameraZ, center.y + cameraZ, center.z + cameraZ);
                camera.lookAt(center);
                controls.target.copy(center);
                controls.update();
            }}

            // Handle window resize
            window.addEventListener('resize', () => {{
                camera.aspect = {width} / {height};
                camera.updateProjectionMatrix();
                renderer.setSize({width}, {height});
            }});
        </script>
    </body>
    </html>
    """
    return html


def geometry_to_mesh_data(geometry: Any) -> dict[str, Any]:
    """Convert a geometry object to mesh data for the viewer.

    This function tessellates the geometry and extracts vertices and faces.

    Args:
        geometry: A geometry object (Build123d, CadQuery, or OCP)

    Returns:
        Dictionary with 'vertices' and 'faces' keys

    Raises:
        ValueError: If geometry type is not supported
    """
    # Try Build123d first
    try:
        from build123d import Part, Shape

        if isinstance(geometry, (Part, Shape)):
            return _build123d_to_mesh(geometry)
    except ImportError:
        pass

    # Try CadQuery
    try:
        import cadquery as cq

        if isinstance(geometry, (cq.Workplane, cq.Shape)):
            return _cadquery_to_mesh(geometry)
    except ImportError:
        pass

    # Try OCP directly
    try:
        from OCP.TopoDS import TopoDS_Shape

        if isinstance(geometry, TopoDS_Shape):
            return _ocp_to_mesh(geometry)
    except ImportError:
        pass

    msg = f"Unsupported geometry type: {type(geometry)}"
    raise ValueError(msg)


def _build123d_to_mesh(geometry: Any) -> dict[str, Any]:
    """Convert Build123d geometry to mesh data.

    Args:
        geometry: Build123d Part or Shape

    Returns:
        Dictionary with vertices and faces
    """
    from OCP.BRepMesh import BRepMesh_IncrementalMesh

    # Get the underlying OCP shape
    if hasattr(geometry, "wrapped"):
        shape = geometry.wrapped
    else:
        shape = geometry

    # Tessellate
    mesh = BRepMesh_IncrementalMesh(shape, 0.1, False, 0.5, True)
    mesh.Perform()

    vertices = []
    faces = []

    from OCP.BRep import BRep_Tool
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    vertex_offset = 0

    while explorer.More():
        face = explorer.Current()
        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation_s(face, location)

        if triangulation:
            # Extract vertices
            for i in range(1, triangulation.NbNodes() + 1):
                node = triangulation.Node(i)
                vertices.append([node.X(), node.Y(), node.Z()])

            # Extract faces
            for i in range(1, triangulation.NbTriangles() + 1):
                triangle = triangulation.Triangle(i)
                n1, n2, n3 = triangle.Get()
                faces.append(
                    [
                        n1 - 1 + vertex_offset,
                        n2 - 1 + vertex_offset,
                        n3 - 1 + vertex_offset,
                    ]
                )

            vertex_offset += triangulation.NbNodes()

        explorer.Next()

    return {"vertices": vertices, "faces": faces, "color": "#3498db"}


def _cadquery_to_mesh(geometry: Any) -> dict[str, Any]:
    """Convert CadQuery geometry to mesh data.

    Args:
        geometry: CadQuery Workplane or Shape

    Returns:
        Dictionary with vertices and faces
    """
    import cadquery as cq

    # Get the shape
    if isinstance(geometry, cq.Workplane):
        shape = geometry.val()
    else:
        shape = geometry

    # Use OCP conversion since CadQuery wraps OCP
    return _ocp_to_mesh(shape.wrapped)


def _ocp_to_mesh(shape: Any) -> dict[str, Any]:
    """Convert OCP TopoDS_Shape to mesh data.

    Args:
        shape: OCP TopoDS_Shape

    Returns:
        Dictionary with vertices and faces
    """
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location

    # Tessellate
    mesh = BRepMesh_IncrementalMesh(shape, 0.1, False, 0.5, True)
    mesh.Perform()

    vertices = []
    faces = []

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    vertex_offset = 0

    while explorer.More():
        face = explorer.Current()
        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation_s(face, location)

        if triangulation:
            # Extract vertices
            for i in range(1, triangulation.NbNodes() + 1):
                node = triangulation.Node(i)
                vertices.append([node.X(), node.Y(), node.Z()])

            # Extract faces
            for i in range(1, triangulation.NbTriangles() + 1):
                triangle = triangulation.Triangle(i)
                n1, n2, n3 = triangle.Get()
                faces.append(
                    [
                        n1 - 1 + vertex_offset,
                        n2 - 1 + vertex_offset,
                        n3 - 1 + vertex_offset,
                    ]
                )

            vertex_offset += triangulation.NbNodes()

        explorer.Next()

    return {"vertices": vertices, "faces": faces, "color": "#3498db"}
