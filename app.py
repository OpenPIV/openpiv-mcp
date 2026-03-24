"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with Streamable HTTP transport.

API Endpoint:
    /mcp - MCP Streamable HTTP endpoint
    /health - Health check endpoint (JSON)

Usage with MCP client:
    Configure your MCP client to connect to:
    https://<your-space>.hf.space/mcp
"""

import os
import sys

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    import uvicorn
    from openpiv_mcp import mcp

    # Get the ASGI app from MCP - this is the cleanest way
    app = mcp.streamable_http_app()

    # Run with uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
