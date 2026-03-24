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

## Quick Start (First Time Users)

### Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up the project
git clone https://huggingface.co/spaces/alexliberzon/openpiv-mcp
cd openpiv-mcp
uv sync
```

### Test with Demo Images

Run the MCP server and test with included demo images:

```bash
cd /home/user/Documents/GitHub/openpiv-mcp
uv run python -c "
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def test():
    img_a = 'demo/test1/exp1_001_a.bmp'
    img_b = 'demo/test1/exp1_001_b.bmp'
    
    server_params = StdioServerParameters(
        command='uv',
        args=['run', 'python', 'src/openpiv_mcp.py'],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Compute PIV
            result = await session.call_tool(
                'compute_piv',
                arguments={
                    'image_a_path': img_a,
                    'image_b_path': img_b,
                    'window_size': 32,
                    'overlap': 16,
                    'dt': 1.0
                }
            )
            print(result.content[0].text)
            
            # Create quiver plot
            import re
            csv_match = re.search(r'/[\w/.]+/piv_results\.csv', result.content[0].text)
            if csv_match:
                plot_result = await session.call_tool(
                    'create_quiver_plot',
                    arguments={'csv_path': csv_match.group(), 'title': 'PIV Velocity Field'}
                )
                print(plot_result.content[0].text)

asyncio.run(test())
"
```

**Expected Output:**
```
PIV computation successful!
Full data saved to: /tmp/piv_results.csv
Summary Statistics:
- Total vectors computed: 660
- Mean U velocity: -0.0814
- Max U velocity: 1.7142
- Max V velocity: 6.9067
The LLM can now use pandas or python tools to plot the data from /tmp/piv_results.csv if requested.

Quiver plot created successfully!
Saved to: /tmp/piv_quiver.png
Plot details:
- Grid size: 30 x 22 vectors
- Velocity range: 4.1213 to 6.9133
- Colormap: viridis
```

### Using with Claude Desktop

1. Open Claude Desktop config:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:
```json
{
  "mcpServers": {
    "openpiv": {
      "command": "uv",
      "args": ["run", "python", "/absolute/path/to/openpiv-mcp/src/openpiv_mcp.py"]
    }
  }
}
```

3. Restart Claude Desktop and ask:
   - "Analyze these two PIV images: [attach image1.bmp, image2.bmp]"
   - "Create a velocity field visualization from the PIV results"

### Using with Qwen Code

Import the client module in your Python code:

```python
from openpiv_client import compute_piv, create_quiver_plot
import asyncio

async def analyze():
    # Compute velocity field from two images
    result = await compute_piv(
        image_a_path="/path/to/image1.bmp",
        image_b_path="/path/to/image2.bmp",
        window_size=32,
        overlap=16
    )
    print(result)
    
    # Create visualization
    plot_result = await create_quiver_plot(
        csv_path="/tmp/piv_results.csv",
        title="My Flow Field"
    )
    print(plot_result)

asyncio.run(analyze())
```

## Usage

### Local Development (stdio mode)

```bash
# Run the MCP server in stdio mode
.venv/bin/python src/openpiv_mcp.py
```

### HuggingFace Spaces (HTTP mode)

**IMPORTANT**: The container may need to be rebuilt. If you see "Not Found" errors:
- Try: `https://alexliberzon-openpiv-mcp.hf.space/mcp` (no trailing slash)
- Use header: `Accept: application/json, text/event-stream`

The MCP endpoint:
```
https://alexliberzon-openpiv-mcp.hf.space/mcp
```

## Testing

```bash
# Test local stdio mode
.venv/bin/python -m pytest tests/test_client.py -v

# Test PIV computation
.venv/bin/python -m pytest tests/test_piv_compute.py -v

# Test HTTP server
.venv/bin/python app.py &
curl http://localhost:7860/health
```

## License

MIT License
