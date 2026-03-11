"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with HTTP transport on Hugging Face Spaces.
The server exposes PIV analysis tools via HTTP.

API Endpoint:
    /mcp - MCP HTTP endpoint (streamable HTTP)
    / - Health check endpoint

Usage with MCP client:
    Configure your MCP client to connect to:
    https://<your-space>.hf.space/mcp
"""

import os
import sys
import logging
import uvicorn

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from openpiv_mcp import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))

# Create FastAPI app with permissive settings for HF Spaces proxy
app = FastAPI(
    title="OpenPIV MCP Server",
    description="Particle Image Velocimetry analysis via MCP protocol",
)

# Health check endpoints for Hugging Face Spaces
@app.get("/", response_class=PlainTextResponse)
async def root():
    """Root health check endpoint."""
    return "OpenPIV MCP Server is running. Connect to /mcp for MCP protocol."

@app.get("/health", response_class=JSONResponse)
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "openpiv-mcp"}

# Mount the MCP streamable HTTP app at /mcp
app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    logger.info(f"Starting OpenPIV MCP Server on {HOST}:{PORT}")
    logger.info("MCP endpoint: /mcp")

    # Configure uvicorn with h11 protocol and permissive proxy settings for HF Spaces
    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        forwarded_allow_ips="*",
        proxy_headers=True,
        server_header=False,
        date_header=False,
        http="h11",
        loop="asyncio",
        trusted_hosts="*",  # Allow all Host headers from HF proxy
    )
    server = uvicorn.Server(config)
    server.run()
