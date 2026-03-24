"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This mounts the MCP server as a Starlette app for Hugging Face Spaces.

API Endpoint:
    /mcp - MCP Streamable HTTP endpoint
    /health - Health check endpoint (JSON)

Usage with MCP client:
    URL: https://alexliberzon-openpiv-mcp.hf.space/mcp
"""

import os
import sys

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    from openpiv_mcp import mcp
    
    # Get the MCP HTTP app
    app = mcp.streamable_http_app()
    
    # Run with uvicorn
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        forwarded_allow_ips="*",
    )
