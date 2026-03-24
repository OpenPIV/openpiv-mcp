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
