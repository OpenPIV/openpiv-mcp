#!/usr/bin/env python3
"""Test client for the OpenPIV MCP server."""

import asyncio
import sys
import os
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


def get_python_cmd():
    """Get the correct python command for the server."""
    venv_python = os.path.join(
        os.path.dirname(__file__), "..", ".venv", "bin", "python"
    )
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


async def test_piv_server():
    server_params = StdioServerParameters(
        command=get_python_cmd(),
        args=["src/openpiv_mcp.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\nServer is working correctly!")


if __name__ == "__main__":
    asyncio.run(test_piv_server())
