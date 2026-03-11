# Using OpenPIV MCP with Qwen Code

## Yes! You can use OpenPIV MCP from Qwen just like Claude!

There are two ways to use the OpenPIV MCP server:

## Option 1: Direct Python API (Recommended for Qwen)

Use the `openpiv_client.py` module directly in your Python code:

```python
import asyncio
from openpiv_client import compute_piv, create_quiver_plot

async def analyze_flow():
    # Compute velocity field from two images
    result = await compute_piv(
        image_a_path="/path/to/image1.tiff",
        image_b_path="/path/to/image2.tiff",
        window_size=32,
        overlap=16,
        dt=1.0
    )
    print(result)
    # Output:
    # PIV computation successful!
    # Full data saved to: /tmp/piv_results.csv
    # Summary Statistics:
    # - Total vectors computed: 1024
    # - Mean U velocity: 0.5234
    # ...
    
    # Create visualization
    plot_result = await create_quiver_plot(
        csv_path="/tmp/piv_results.csv",
        title="My Flow Field",
        scale=50,
        cmap="viridis"
    )
    print(plot_result)
    # Output:
    # Quiver plot created successfully!
    # Saved to: /tmp/piv_quiver.png

# Run the analysis
asyncio.run(analyze_flow())
```

## Option 2: MCP Client Integration

If you want to use MCP protocol integration (like Claude Desktop):

```python
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def use_mcp():
    server_params = StdioServerParameters(
        command="python",
        args=["src/openpiv_mcp.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"{tool.name}: {tool.description}")
            
            # Call a tool
            result = await session.call_tool(
                "compute_piv",
                arguments={
                    "image_a_path": "/path/to/image1.tiff",
                    "image_b_path": "/path/to/image2.tiff",
                }
            )
            print(result.content[0].text)

asyncio.run(use_mcp())
```

## Example: Complete PIV Analysis Workflow

Here's a complete example that Qwen can help you write:

```python
#!/usr/bin/env python3
"""Example PIV analysis workflow."""

import asyncio
from openpiv_client import compute_piv, create_quiver_plot

async def main():
    # Step 1: Compute velocity field
    print("Computing PIV...")
    piv_result = await compute_piv(
        image_a_path="data/frame_a.tiff",
        image_b_path="data/frame_b.tiff",
        window_size=32,
        overlap=16
    )
    print(piv_result)
    
    # Step 2: Create visualization
    print("\nCreating quiver plot...")
    # Extract CSV path from result
    csv_path = "/tmp/piv_results.csv"  # or parse from piv_result
    plot_result = await create_quiver_plot(
        csv_path=csv_path,
        title="Channel Flow at Re=1000",
        scale=100
    )
    print(plot_result)
    
    # Step 3: The PNG is saved and can be displayed
    print("\nDone! Check /tmp/piv_quiver.png")

if __name__ == "__main__":
    asyncio.run(main())
```

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

## Available Tools

| Tool | Description |
|------|-------------|
| `compute_piv` | Compute velocity fields from image pairs |
| `create_quiver_plot` | Generate vector field visualizations |

## Parameters

### compute_piv
- `image_a_path`: Path to first image (required)
- `image_b_path`: Path to second image (required)
- `window_size`: Interrogation window size (default: 32)
- `overlap`: Overlap between windows (default: 16)
- `dt`: Time delay between frames (default: 1.0)
- `output_dir`: Output directory (default: temp directory)

### create_quiver_plot
- `csv_path`: Path to PIV results CSV (required)
- `output_path`: Output PNG path (default: same as CSV dir)
- `title`: Plot title (default: "PIV Velocity Field")
- `scale`: Arrow scale factor (default: 50)
- `width`: Arrow width (default: 0.003)
- `cmap`: Colormap (default: "viridis")
