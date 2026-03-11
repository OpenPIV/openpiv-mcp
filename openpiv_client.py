#!/usr/bin/env python3
"""
OpenPIV MCP Client - Use PIV analysis directly in your Python code.

This module provides a simple interface to use the OpenPIV MCP server
from your Python applications.
"""

import asyncio
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


async def compute_piv(
    image_a_path: str,
    image_b_path: str,
    window_size: int = 32,
    overlap: int = 16,
    dt: float = 1.0,
    output_dir: str = ""
) -> str:
    """
    Compute PIV velocity field from two images.
    
    Args:
        image_a_path: Path to first image
        image_b_path: Path to second image
        window_size: Interrogation window size (default 32)
        overlap: Overlap between windows (default 16)
        dt: Time delay between frames (default 1.0)
        output_dir: Output directory for results
        
    Returns:
        Result message with output path and statistics
    """
    server_params = StdioServerParameters(
        command="python",
        args=[os.path.join(os.path.dirname(__file__), "src", "openpiv_mcp.py")],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "compute_piv",
                arguments={
                    "image_a_path": image_a_path,
                    "image_b_path": image_b_path,
                    "window_size": window_size,
                    "overlap": overlap,
                    "dt": dt,
                    "output_dir": output_dir
                }
            )
            return result.content[0].text if result.content else "No result"


async def create_quiver_plot(
    csv_path: str,
    output_path: str = "",
    title: str = "PIV Velocity Field",
    scale: int = 50,
    width: float = 0.003,
    cmap: str = "viridis"
) -> str:
    """
    Create a quiver plot from PIV results.
    
    Args:
        csv_path: Path to PIV results CSV
        output_path: Output path for PNG
        title: Plot title
        scale: Arrow scale factor
        width: Arrow width
        cmap: Colormap
        
    Returns:
        Result message with output path
    """
    server_params = StdioServerParameters(
        command="python",
        args=[os.path.join(os.path.dirname(__file__), "src", "openpiv_mcp.py")],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "create_quiver_plot",
                arguments={
                    "csv_path": csv_path,
                    "output_path": output_path,
                    "title": title,
                    "scale": scale,
                    "width": width,
                    "cmap": cmap
                }
            )
            return result.content[0].text if result.content else "No result"


async def main():
    """Example usage."""
    print("=" * 60)
    print("OpenPIV MCP Client Demo")
    print("=" * 60)
    
    # Example: Compute PIV (using demo images if they exist)
    demo_dir = os.path.join(os.path.dirname(__file__), "demo", "test1")
    img_a = os.path.join(demo_dir, "exp1_001_a.tiff")
    img_b = os.path.join(demo_dir, "exp1_001_b.tiff")
    
    if os.path.exists(img_a) and os.path.exists(img_b):
        print(f"\n1. Computing PIV on demo images...")
        result = await compute_piv(img_a, img_b)
        print(f"\n   Result:\n{result}")
        
        # Extract CSV path from result
        if "piv_results.csv" in result:
            import re
            csv_match = re.search(r'/[\w/.]+/piv_results\.csv', result)
            if csv_match:
                csv_path = csv_match.group()
                print(f"\n2. Creating quiver plot from {csv_path}...")
                plot_result = await create_quiver_plot(csv_path)
                print(f"\n   Result:\n{plot_result}")
    else:
        print(f"Demo images not found at {demo_dir}")
        print("\nTo use PIV analysis, call:")
        print("""
import asyncio
from openpiv_client import compute_piv, create_quiver_plot

async def analyze():
    # Compute velocity field
    result = await compute_piv(
        image_a_path="/path/to/image1.tiff",
        image_b_path="/path/to/image2.tiff",
        window_size=32,
        overlap=16
    )
    print(result)
    
    # Create visualization
    plot_result = await create_quiver_plot(
        csv_path="/path/to/piv_results.csv",
        title="My Flow Field"
    )
    print(plot_result)

asyncio.run(analyze())
        """)


if __name__ == "__main__":
    asyncio.run(main())
