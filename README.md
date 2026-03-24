---
title: OpenPIV MCP Server
emoji: 🌊
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: edge
pinned: false
license: mit
---

# OpenPIV MCP Server

Particle Image Velocimetry (PIV) analysis via MCP protocol.

## Features

- **compute_piv**: Compute velocity fields from image pairs
- **create_quiver_plot**: Generate vector field visualizations
- **Web UI**: Interactive Gradio interface for uploading images and viewing results
- **MCP Protocol**: Connect to Claude Desktop, Cursor, Windsurf, and other MCP clients

## Quick Start

### Option 1: Local MCP Server (Recommended for Development)

Run the MCP server locally using stdio transport:

```bash
# Clone and install
git clone https://huggingface.co/spaces/alexliberzon/openpiv-mcp
cd openpiv-mcp
pip install -r requirements.txt

# Run the MCP server
python src/openpiv_mcp.py
```

**Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "openpiv": {
      "command": "python",
      "args": ["/absolute/path/to/openpiv-mcp/src/openpiv_mcp.py"]
    }
  }
}
```

### Option 2: Hugging Face Spaces (Remote HTTP)

The server is deployed on Hugging Face Spaces with both web UI and MCP endpoint:

- **Web UI**: https://alexliberzon-openpiv-mcp.hf.space
- **MCP Endpoint**: `https://alexliberzon-openpiv-mcp.hf.space/gradio_api/mcp/`

**MCP Client Config:**
```json
{
  "mcpServers": {
    "openpiv": {
      "url": "https://alexliberzon-openpiv-mcp.hf.space/gradio_api/mcp/"
    }
  }
}
```

**Note:** When using the remote MCP server, images must be provided as:
- HTTP/HTTPS URLs (e.g., `https://example.com/image.png`)
- Base64 data URLs (e.g., `data:image/png;base64,iVBOR...`)

### Option 3: Web UI Only

Visit https://alexliberzon-openpiv-mcp.hf.space to use the interactive web interface:
1. Upload two consecutive frames (Frame A and Frame B)
2. Adjust parameters (window size, overlap, time delay)
3. Click "Compute PIV" to get velocity field data
4. Use the "Quiver Plot" tab to visualize results

## API Reference

### compute_piv

Compute Particle Image Velocimetry velocity field from two images.

**Parameters:**
- `image_a` (str): Image URL, base64 data URL, or file path (local only)
- `image_b` (str): Image URL, base64 data URL, or file path (local only)
- `window_size` (int): Interrogation window size (default: 32)
- `overlap` (int): Overlap between windows (default: 16)
- `dt` (float): Time delay between frames (default: 1.0)

**Returns:** Summary statistics and CSV file path

### create_quiver_plot

Create a quiver (vector field) plot from PIV results.

**Parameters:**
- `csv_file` (str): Path to PIV results CSV file
- `title` (str): Plot title (default: "PIV Velocity Field")
- `scale` (int): Quiver scale factor (default: 50)
- `cmap` (str): Colormap (default: "viridis")

**Returns:** PIL Image of the quiver plot

## Example Output

```
**PIV computation successful!**

**Summary Statistics:**
- Total vectors computed: 660
- Valid vectors (s2n>1): 580
- Mean U velocity: -0.0814
- Max U velocity: 1.7142
- Max V velocity: 6.9067
```

## Local Testing

```bash
# Test with demo images
python -c "
from openpiv_client import compute_piv, create_quiver_plot
import asyncio

async def test():
    result = await compute_piv(
        image_a_path='demo/test1/exp1_001_a.bmp',
        image_b_path='demo/test1/exp1_001_b.bmp'
    )
    print(result)

asyncio.run(test())
"
```

## License

MIT License
