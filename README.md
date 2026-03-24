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

Connect your MCP client to:
```
https://alexliberzon-openpiv-mcp.hf.space/mcp
```

Note: The MCP endpoint requires both `application/json` and `text/event-stream` in the Accept header.

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
