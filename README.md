# OpenPIV MCP Server

A Model Context Protocol (MCP) server that provides Particle Image Velocimetry (PIV) analysis tools. Analyze flow fields from image pairs and visualize velocity vectors.

## Features

- **`compute_piv`** - Compute PIV velocity fields from two image frames
- **`create_quiver_plot`** - Generate vector field visualization (PNG) from PIV results

## Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/openpiv/openpiv-mcp.git
cd openpiv-mcp

# Install dependencies with uv
uv sync
```

## Running the MCP Server

### Direct execution with uv

```bash
uv run python src/openpiv_mcp.py
```

The server runs over stdio, which is the standard transport for local MCP clients.

### Configure in Claude Desktop

Add this to your Claude Desktop MCP configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "openpiv": {
      "command": "uv",
      "args": ["run", "python", "src/openpiv_mcp.py"],
      "cwd": "/absolute/path/to/openpiv-mcp"
    }
  }
}
```

## Usage

### Tool: `compute_piv`

Computes PIV velocity field from two image frames.

```python
compute_piv(
    image_a_path: str,       # Path to first image frame
    image_b_path: str,       # Path to second image frame
    window_size: int = 32,   # Interrogation window size (pixels)
    overlap: int = 16,       # Window overlap (pixels)
    dt: float = 1.0,         # Time delay between frames
    output_dir: str = ""     # Output directory (default: /tmp)
) -> str
```

**Returns:** Summary statistics and path to CSV results file.

### Tool: `create_quiver_plot`

Creates a quiver (vector field) plot from PIV results.

```python
create_quiver_plot(
    csv_path: str,              # Path to PIV results CSV
    output_path: str = "",      # Output PNG path (default: same as CSV)
    title: str = "PIV Velocity Field",
    scale: int = 50,            # Arrow scale (higher = shorter arrows)
    width: float = 0.003,       # Arrow width
    cmap: str = "viridis"       # Colormap for velocity magnitude
) -> str
```

**Returns:** Path to generated PNG file.

## Testing

### Run all tests

```bash
# Test MCP server connection
uv run python test_client.py

# Test PIV computation with sample images
uv run python test_piv_compute.py

# Test quiver plot generation
uv run python test_quiver.py
```

### Test files

| File | Description |
|------|-------------|
| `test_client.py` | Verifies MCP server connection and lists available tools |
| `test_piv_compute.py` | Runs PIV analysis on sample images from openpiv package |
| `test_quiver.py` | Generates quiver plot from PIV results |

### Expected output

```
PIV computation successful!
Full data saved to: /tmp/piv_results.csv
Summary Statistics:
- Total vectors computed: 660
- Mean U velocity: -0.0814
- Max U velocity: 1.7142
- Max V velocity: 6.9067
```

## Output Files

- **`piv_results.csv`** - Velocity field data (x, y, u, v, s2n)
- **`piv_quiver.png`** - Vector field visualization

## Dependencies

| Package | Version |
|---------|---------|
| mcp | >=1.26.0 |
| openpiv | >=0.25.1 |
| numpy | >=2.4.3 |
| pandas | >=3.0.1 |
| matplotlib | (auto-installed) |

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or submit a PR.
