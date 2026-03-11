"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with HTTP transport on Hugging Face Spaces.
The server exposes PIV analysis tools via HTTP.

API Endpoint:
    /mcp - MCP HTTP endpoint (streamable HTTP)

Usage with MCP client:
    Configure your MCP client to connect to:
    https://<your-space>.hf.space/mcp
"""

import os
import logging
import asyncio
from openpiv_mcp import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))

# Create the ASGI app for HTTP transport
app = mcp.streamable_http_app()


async def serve():
    """Serve the app using hypercorn (more permissive with Host headers)."""
    from hypercorn.config import Config
    from hypercorn.asyncio import serve as hypercorn_serve
    
    config = Config()
    config.bind = [f"{HOST}:{PORT}"]
    config.accesslog = "-"
    config.errorlog = "-"
    
    logger.info(f"Starting OpenPIV MCP Server on {HOST}:{PORT}")
    logger.info("MCP endpoint: /mcp")
    
    await hypercorn_serve(app, config)


if __name__ == "__main__":
    asyncio.run(serve())
