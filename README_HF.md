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

## Usage

### Option 1: Local MCP Server (Recommended)

Run the server locally using stdio transport:

```bash
# Clone the repository
git clone https://huggingface.co/spaces/alexliberzon/openpiv-mcp
cd openpiv-mcp

# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python src/openpiv_mcp.py
```

Then connect your MCP client (Claude Desktop, etc.) using stdio transport:

```json
{
  "mcpServers": {
    "openpiv": {
      "command": "python",
      "args": ["src/openpiv_mcp.py"],
      "cwd": "/path/to/openpiv-mcp"
    }
  }
}
```

### Option 2: HTTP/SSE Transport

The server also supports HTTP/SSE transport for remote connections.

Connect to: `https://alexliberzon-openpiv-mcp.hf.space/mcp`

**Note:** HTTP transport requires an MCP client that supports streamable HTTP or SSE transport.

## Example: Using with Claude Desktop

1. Install Claude Desktop
2. Open config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
3. Add the MCP server configuration:

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

4. Restart Claude Desktop
5. Ask Claude to analyze PIV images!

## Example: PIV Analysis

Once connected, you can ask the MCP server to:

- "Analyze these two PIV images and compute the velocity field"
- "Create a quiver plot from this PIV results CSV"
- "What's the maximum velocity in this flow field?"

## License

MIT License
