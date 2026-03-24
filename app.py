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
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse, PlainTextResponse
    from starlette.routing import Route, Mount
    from openpiv_mcp import mcp

    # Create MCP app first to initialize session_manager
    mcp_app = mcp.streamable_http_app()

    # Get the session manager for lifespan
    session_manager = mcp.session_manager

    # Create health check endpoints
    async def health(request):
        return JSONResponse({"status": "healthy", "service": "openpiv-mcp"})

    async def root(request):
        return PlainTextResponse(
            "OpenPIV MCP Server is running. Connect to /mcp for MCP protocol."
        )

    # Create app with proper lifespan to initialize MCP session manager
    async def lifespan(app):
        async with session_manager.run():
            yield

    # Create combined app with health endpoints and proper lifespan
    app = Starlette(
        routes=[
            Route("/", root),
            Route("/health", health),
            Mount("/", app=mcp_app),
        ],
        lifespan=lifespan,
    )

    # Run with uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
