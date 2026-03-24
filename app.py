"""
Hugging Face Spaces entry point for OpenPIV MCP Server.

This app runs the MCP server with Streamable HTTP transport.

API Endpoint:
    /mcp - MCP Streamable HTTP endpoint (no trailing slash)
    /health - Health check endpoint (JSON)

Usage with MCP client:
    IMPORTANT: Use exactly /mcp (NO trailing slash)
    Example: https://alexliberzon-openpiv-mcp.hf.space/mcp
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
    from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
    from starlette.routing import Route
    from openpiv_mcp import mcp

    # Create MCP app - this is the core MCP server
    mcp_app = mcp.streamable_http_app()
    session_manager = mcp.session_manager

    # Health check endpoints
    async def health(request):
        return JSONResponse({"status": "healthy", "service": "openpiv-mcp"})

    async def root(request):
        return PlainTextResponse(
            "OpenPIV MCP Server is running. Connect to /mcp for MCP protocol."
        )

    # Redirect /mcp/ to /mcp to avoid 404
    async def redirect_mcp_slash(request):
        return RedirectResponse(url="/mcp", status_code=307)

    # Create app with proper lifespan
    async def lifespan(app):
        async with session_manager.run():
            yield

    # Create app with explicit routes to control routing behavior
    app = Starlette(
        routes=[
            Route("/", root),
            Route("/health", health),
            Route("/mcp/", redirect_mcp_slash),  # Redirect /mcp/ back to /mcp
        ],
        lifespan=lifespan,
    )

    # Mount MCP at root - MCP's /mcp becomes /mcp on host
    app.mount("/", mcp_app)

    # Run with uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
