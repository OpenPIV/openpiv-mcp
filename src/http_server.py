"""
HTTP Server wrapper for OpenPIV MCP Server.

This module provides an HTTP endpoint for the OpenPIV MCP server,
enabling remote clients to connect via HTTP instead of stdio.

Usage:
    uv run python src/http_server.py
    
Or on Hugging Face Spaces, it runs automatically via app.py
"""

import os
import uvicorn
from openpiv_mcp import mcp

# Get host/port from environment (for Hugging Face Spaces)
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))

# Create the ASGI app for HTTP transport
app = mcp.streamable_http_app()

if __name__ == "__main__":
    print(f"Starting OpenPIV MCP Server on {HOST}:{PORT}")
    print("Endpoint: http://{HOST}:{PORT}/mcp")
    
    # Run with uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
