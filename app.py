"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with SSE transport on Hugging Face Spaces.

API Endpoint:
    /mcp - MCP SSE endpoint
    / - Health check endpoint

Usage with MCP client:
    Configure your MCP client to connect to:
    https://<your-space>.hf.space/mcp
"""

import os
import sys
import logging

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from openpiv_mcp import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 7860))

# Get the MCP SSE app
mcp_sse_app = mcp.sse_app()

# Create a FastAPI wrapper for health checks
app = FastAPI(
    title="OpenPIV MCP Server",
    description="Particle Image Velocimetry analysis via MCP protocol",
)

# Health check endpoints
@app.get("/", response_class=PlainTextResponse)
async def root():
    """Root health check endpoint."""
    return "OpenPIV MCP Server is running. Connect to /mcp for MCP protocol."

@app.get("/health", response_class=JSONResponse)
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "openpiv-mcp"}

# Mount MCP app at /mcp
app.mount("/mcp", mcp_sse_app)

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting OpenPIV MCP Server on {HOST}:{PORT}")
    logger.info("MCP endpoint: /mcp")

    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        forwarded_allow_ips="*",
        proxy_headers=True,
        http="h11",
    )
    server = uvicorn.Server(config)
    server.run()
