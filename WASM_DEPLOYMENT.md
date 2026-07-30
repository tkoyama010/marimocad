# WebAssembly (WASM) Deployment Guide

This guide explains how to deploy marimocad examples as WebAssembly applications that run entirely in the browser.

## Overview

marimocad supports WebAssembly deployment through [marimo](https://marimo.io/) notebooks and [Pyodide](https://pyodide.org/), allowing users to:

- Try marimocad without any local installation
- Share interactive CAD demos via URL
- Embed CAD examples in websites
- Create educational materials
- Build portfolio/showcase projects

## WASM Example

We provide a WASM-optimized example at `examples/wasm_demo.py` that demonstrates:

- ✅ Reactive parameter controls
- ✅ Real-time calculations
- ✅ Interactive UI components
- ✅ **Interactive 3D visualization** with Plotly
- ✅ Basic geometry creation (Box, Cylinder)
- ✅ Parametric modeling with real-time updates

### Try the Live Demo

**🌐 [Live WASM Demo](https://tkoyama010.github.io/marimocad/)**

## Running Locally

### Test the WASM Example in Desktop Mode

```bash
# Install dependencies
pip install marimo build123d plotly

# Run the WASM demo locally with full 3D visualization
marimo edit examples/wasm_demo.py
```

The demo includes:
- **Interactive sliders** for adjusting geometry parameters
- **Live 3D visualization** using Plotly (rotate, pan, zoom)
- **Real-time updates** as you change parameters
- **Geometry metadata** showing vertices, edges, and faces

### Export to WASM HTML

```bash
# Export as read-only app
marimo export html-wasm examples/wasm_demo.py -o output --mode run

# Export as editable notebook
marimo export html-wasm examples/wasm_demo.py -o output --mode edit

# Export with code visible
marimo export html-wasm examples/wasm_demo.py -o output --mode run --show-code
```

The exported files can be served from any static hosting service.

## GitHub Pages Deployment

### Automatic Deployment

This repository uses GitHub Actions to automatically deploy WASM demos:

1. **Trigger:** Push to `main` branch or run workflow manually
2. **Build:** Exports `examples/wasm_demo.py` to WASM HTML
3. **Deploy:** Publishes to GitHub Pages at `https://tkoyama010.github.io/marimocad/`

See `.github/workflows/deploy-wasm.yml` for the workflow configuration.

### Manual Deployment

To deploy manually:

```bash
# 1. Export the notebook
marimo export html-wasm examples/wasm_demo.py -o wasm-output --mode run

# 2. Create index.html (landing page)
# See .github/workflows/deploy-wasm.yml for template

# 3. Add .nojekyll to prevent Jekyll processing
touch wasm-output/.nojekyll

# 4. Push to gh-pages branch or configure GitHub Pages
```

## WASM Compatibility

### What Works

✅ **Core Python:** Standard library, math operations
✅ **Marimo:** Full reactive notebook functionality
✅ **UI Components:** Sliders, inputs, buttons, charts
✅ **Data Processing:** NumPy, Pandas (via Pyodide)
✅ **Visualization:** Matplotlib, Altair, Plotly
✅ **3D Visualization:** Interactive 3D viewing with Plotly (NEW!)
✅ **Build123d:** Geometry creation (requires OCP.wasm)
✅ **Mesh Extraction:** Convert Build123d geometry to triangular meshes

### Current Limitations

⚠️ **3D Rendering:**
- Interactive 3D visualization now available via Plotly!
- Requires Build123d and Plotly packages
- Desktop version uses Build123d's native 3D viewer (ocp-tessellate)
- For best performance, use moderate complexity geometry

⚠️ **Performance:**
- WASM execution is slower than native Python (2-5x overhead)
- First load requires downloading Pyodide runtime (~10-30 seconds)
- 3D visualization performs well for moderate complexity models
- Complex CAD operations may be slow

⚠️ **File Operations:**
- No direct filesystem access in browser
- Export to STEP/STL files requires workarounds
- File uploads possible via browser APIs

⚠️ **Dependencies:**
- Only pure Python packages or WASM-ported packages work
- C/C++ extensions need WASM compilation
- Build123d depends on OCP.wasm being available

### OCP.wasm Integration Status

**Build123d + WASM:** Build123d CAN run in browser via [OCP.wasm](https://github.com/yeicor/OCP.wasm), which ports OpenCascade to WebAssembly.

**Current Status:**
- OCP.wasm exists and works with Build123d
- Not yet integrated in standard Pyodide distribution
- Requires custom Pyodide build or manual package loading

**3D Visualization Solution:**
- ✅ **Implemented:** Interactive 3D visualization via Plotly
- ✅ **Works now:** Browser-based 3D rendering without OCP.wasm
- ✅ **Features:** Rotate, pan, zoom, real-time updates
- Uses mesh extraction and Plotly's 3D mesh plotting

**Future Plans:**
- Monitor OCP.wasm development for enhanced rendering
- Continue improving Plotly-based visualization
- Add more export formats and rendering options

## 3D Visualization Features

The WASM demo now includes full interactive 3D visualization:

### Features
- **Interactive Controls:** Rotate, pan, zoom with mouse/touch
- **Real-time Updates:** 3D view updates as you adjust parameters
- **Multiple Geometries:** View box, cylinder, and combined shapes
- **High Quality:** Mesh-based rendering with proper lighting
- **Browser Native:** No plugins or external viewers needed

### Technology Stack
- **Mesh Extraction:** Build123d → OCP tessellation → NumPy arrays
- **Visualization:** Plotly 3D mesh plotting
- **Integration:** Marimo's `mo.ui.plotly()` component
- **Performance:** Optimized for browser execution

### Usage Example

```python
from build123d import Box, BuildPart
from marimocad.visualization import create_plotly_figure
import marimo as mo

# Create geometry
with BuildPart() as my_box:
    Box(10, 10, 10)

# Create 3D figure
fig = create_plotly_figure(
    my_box.part,
    color='lightblue',
    title='My Box',
    show_edges=False
)

# Display in marimo
mo.ui.plotly(fig)
```

## Optimization Tips

### Reduce Bundle Size

```python
# Import only what you need
from build123d import Box, Cylinder  # Good
# from build123d import *              # Avoid
```

### Improve Loading Time

1. **Use CDN for common packages:** Pyodide caches packages
2. **Minimize custom packages:** Fewer imports = faster load
3. **Lazy imports:** Import heavy libraries only when needed
4. **Optimize geometry:** Simpler shapes = faster computation

### Best Practices

- Keep models simple for WASM demos
- Use desktop version for production work
- Cache geometry calculations when possible
- Test on multiple browsers and devices

## Browser Compatibility

**Supported Browsers:**
- ✅ Chrome/Edge (recommended, best performance)
- ✅ Firefox
- ✅ Safari (may be slower)

**Requirements:**
- WebAssembly support (all modern browsers)
- JavaScript enabled
- Minimum 2GB RAM recommended
- Stable internet connection (first load)

## Troubleshooting

### Demo Won't Load

- **Check browser console** for errors
- **Wait for Pyodide** to download (~10-30 seconds)
- **Try different browser** if persistent issues
- **Clear browser cache** and reload

### Slow Performance

- **Expected:** WASM is slower than native Python
- **Use desktop version** for complex operations
- **Simplify geometry** for browser demos
- **Close other tabs** to free memory

### Missing Build123d Features

- **OCP.wasm not available:** Some features won't work
- **Desktop version** has full functionality
- **Check browser console** for import errors

## Alternative Deployment Options

### Static Hosting

Deploy exported WASM HTML to:
- **GitHub Pages** (free, recommended)
- **Netlify** (free tier available)
- **Vercel** (free tier available)
- **AWS S3 + CloudFront**
- Any static file hosting service

### Custom Domain

Configure GitHub Pages with custom domain:
1. Add CNAME file to `wasm-output/`
2. Configure DNS records
3. Enable HTTPS in GitHub settings

## Examples and Templates

### Official marimo Template

Fork the official template: [marimo-gh-pages-template](https://github.com/marimo-team/marimo-gh-pages-template)

### Community Examples

- [marimo WASM demos](https://marimo.io/gallery)
- [OCP.wasm examples](https://github.com/yeicor/OCP.wasm)

## Contributing

Want to improve the WASM demo?

1. Test new features in desktop mode first
2. Verify WASM compatibility
3. Optimize for browser performance
4. Update this documentation
5. Submit a pull request

## Resources

- **[marimo WASM Guide](https://docs.marimo.io/guides/wasm/)** - Official documentation
- **[Pyodide](https://pyodide.org/)** - Python in the browser
- **[OCP.wasm](https://github.com/yeicor/OCP.wasm)** - Build123d in browser
- **[GitHub Pages](https://pages.github.com/)** - Free static hosting

## Support

- **Issues:** [GitHub Issues](https://github.com/tkoyama010/marimocad/issues)
- **Discussions:** [GitHub Discussions](https://github.com/tkoyama010/marimocad/discussions)
- **marimo Discord:** [Join](https://discord.gg/JE7nhX6mD8)

---

**Note:** WASM deployment is an experimental feature. For production CAD work, use the desktop version with full Build123d support.
