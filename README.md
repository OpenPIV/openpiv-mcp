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

### Hugging Face Spaces (Recommended)

The server is deployed on Hugging Face Spaces with both web UI and MCP endpoint:

- **Web UI**: https://alexliberzon-openpiv-mcp.hf.space
- **MCP Endpoint**: `https://alexliberzon-openpiv-mcp.hf.space/gradio_api/mcp/`

### Using with MCP Clients

#### Claude Desktop / Cursor / Windsurf

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "openpiv": {
      "url": "https://alexliberzon-openpiv-mcp.hf.space/gradio_api/mcp/",
      "description": "PIV analysis for fluid dynamics"
    }
  }
}
```

**Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Qwen Code (Python)

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio

async def analyze():
    url = "https://alexliberzon-openpiv-mcp.hf.space/gradio_api/mcp/"
    
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print([t.name for t in tools.tools])
            
            # Call compute_piv tool
            result = await session.call_tool(
                "compute_piv",
                arguments={
                    "image_a": "path/to/image1.png",
                    "image_b": "path/to/image2.png",
                    "window_size": 32,
                    "overlap": 16,
                    "dt": 1.0
                }
            )
            print(result.content[0].text)

asyncio.run(analyze())
```

### Local Development

```bash
# Clone the repository
git clone https://huggingface.co/spaces/alexliberzon/openpiv-mcp
cd openpiv-mcp

# Install dependencies
pip install -r requirements.txt

# Run the Gradio app with MCP server
python gradio_app.py
```

The app will be available at `http://localhost:7860` and MCP endpoint at `/gradio_api/mcp/`

## Web UI Usage

1. **PIV Analysis Tab**:
   - Upload two consecutive frames (Frame A and Frame B)
   - Adjust window size, overlap, and time delay parameters
   - Click "Compute PIV" to get velocity field data

2. **Quiver Plot Tab**:
   - Upload the CSV file from PIV analysis
   - Adjust plot title and arrow scale
   - Click "Create Quiver Plot" to visualize the velocity field

## API Reference

### compute_piv

Compute Particle Image Velocimetry velocity field from two images.

**Parameters:**
- `image_a` (PIL.Image): First image frame
- `image_b` (PIL.Image): Second image frame
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

## License

MIT License
