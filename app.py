"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with SSE transport (more compatible with HF proxy).

API Endpoint:
    /mcp - MCP SSE endpoint (with /mcp/ redirect)
    /health - Health check endpoint (JSON)

Usage with MCP client:
    Use: https://alexliberzon-openpiv-mcp.hf.space/mcp
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
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
    from openpiv_mcp import mcp

    # Get MCP SSE app
    mcp_sse_app = mcp.sse_app()

    # Create FastAPI app
    app = FastAPI(
        title="OpenPIV MCP Server",
        description="Particle Image Velocimetry analysis via MCP protocol",
    )

    # Health check endpoints
    @app.get("/")
    def root():
        return "OpenPIV MCP Server is running. Connect to /mcp for MCP protocol."

    @app.get("/health")
    def health():
        return JSONResponse({"status": "healthy", "service": "openpiv-mcp"})

    # Add redirect from /mcp/ to /mcp to fix trailing slash issue
    @app.get("/mcp/")
    def redirect_mcp():
        return RedirectResponse(url="/mcp", status_code=307)

    # Mount MCP at /mcp - now /mcp/ goes to redirect handler first
    app.mount("/mcp", mcp_sse_app)

    # Run with uvicorn - allow HF proxy
    uvicorn.run(app, host=HOST, port=PORT, forwarded_allow_ips="*")
