#!/usr/bin/env python3
"""Test the compute_piv tool with sample images."""

import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def test_compute_piv():
    server_params = StdioServerParameters(
        command="python",
        args=["src/openpiv_mcp.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get test images from openpiv package
            import importlib.resources as pkg
            im1 = str(pkg.files("openpiv").joinpath("data/test1/exp1_001_a.bmp"))
            im2 = str(pkg.files("openpiv").joinpath("data/test1/exp1_001_b.bmp"))
            
            print(f"Using test images:")
            print(f"  Image A: {im1}")
            print(f"  Image B: {im2}")
            print()
            
            # Call compute_piv tool
            result = await session.call_tool(
                "compute_piv",
                arguments={
                    "image_a_path": im1,
                    "image_b_path": im2,
                    "window_size": 32,
                    "overlap": 16,
                    "dt": 1.0
                }
            )
            
            print("Result:")
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(test_compute_piv())
