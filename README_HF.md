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

## Quick Start

### Using with Python (Recommended)

```python
import asyncio
from openpiv_client import compute_piv, create_quiver_plot

async def analyze():
    # Compute velocity field
    result = await compute_piv(
        image_a_path="/path/to/image1.tiff",
        image_b_path="/path/to/image2.tiff"
    )
    print(result)
    
    # Create visualization
    await create_quiver_plot(
        csv_path="/tmp/piv_results.csv",
        title="My Flow Field"
    )

asyncio.run(analyze())
```

### Using with MCP Clients

#### Claude Desktop

1. Open config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add configuration:
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

3. Restart Claude Desktop

#### Qwen Code

Use the `openpiv_client.py` module directly in your Python code. See [USAGE_QWEN.md](USAGE_QWEN.md) for details.

## Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/alexliberzon/openpiv-mcp
cd openpiv-mcp

# Install dependencies
pip install -r requirements.txt

# Test the installation
python test_mcp_connection.py
```

## API Reference

### compute_piv

Compute Particle Image Velocimetry velocity field from two images.

**Parameters:**
- `image_a_path` (str): Path to first image frame
- `image_b_path` (str): Path to second image frame
- `window_size` (int): Interrogation window size (default: 32)
- `overlap` (int): Overlap between windows (default: 16)
- `dt` (float): Time delay between frames (default: 1.0)
- `output_dir` (str): Output directory for CSV (default: temp directory)

**Returns:** String with results path and statistics

### create_quiver_plot

Create a quiver (vector field) plot from PIV results.

**Parameters:**
- `csv_path` (str): Path to PIV results CSV file
- `output_path` (str): Output path for PNG (default: CSV directory)
- `title` (str): Plot title (default: "PIV Velocity Field")
- `scale` (int): Quiver scale factor (default: 50)
- `width` (float): Arrow width (default: 0.003)
- `cmap` (str): Colormap (default: "viridis")

**Returns:** String with output path and plot details

## Example Output

```
PIV computation successful!
Full data saved to: /tmp/piv_results.csv
Summary Statistics:
- Total vectors computed: 1024
- Mean U velocity: 0.5234
- Max U velocity: 1.2345
- Max V velocity: 0.8765

Quiver plot created successfully!
Saved to: /tmp/piv_quiver.png
Plot details:
- Grid size: 32 x 32 vectors
- Velocity range: 0.0012 to 1.2345
- Colormap: viridis
```

## License

MIT License
