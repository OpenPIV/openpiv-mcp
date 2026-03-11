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
import uvicorn
from openpiv_mcp import mcp
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))


class HostHeaderFix:
    """Middleware to fix Host header from Hugging Face proxy."""
    
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            # Get headers from scope
            headers = dict(scope.get("headers", []))
            
            # Check for x-proxied-host header from HF proxy
            proxied_host = headers.get(b"x-proxied-host")
            if proxied_host:
                # Replace host header with the proxied host
                headers[b"host"] = proxied_host
                scope["headers"] = list(headers.items())
        
        await self.app(scope, receive, send)


# Create the ASGI app for HTTP transport
app = mcp.streamable_http_app()

# Add the Host header fix middleware
app.add_middleware(HostHeaderFix)

if __name__ == "__main__":
    logger.info(f"Starting OpenPIV MCP Server on {HOST}:{PORT}")
    logger.info("MCP endpoint: /mcp")

    # Run with uvicorn - allow all forwarded IPs for Hugging Face Spaces
    uvicorn.run(app, host=HOST, port=PORT, forwarded_allow_ips="*")
