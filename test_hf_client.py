#!/usr/bin/env python3
"""Test client for the OpenPIV MCP server on Hugging Face Spaces."""

import asyncio
import httpx

async def test_hf_mcp():
    """Test the MCP server on HF Spaces using HTTP."""
    base_url = "https://alexliberzon-openpiv-mcp.hf.space"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test health endpoint
        print("Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"Health: {response.json()}")
        
        # Test root endpoint
        print("\nTesting root endpoint...")
        response = await client.get(f"{base_url}/")
        print(f"Root: {response.text}")
        
        # Test MCP endpoint (initialize session)
        print("\nTesting MCP endpoint...")
        try:
            response = await client.post(
                f"{base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"}
                    },
                    "id": 1
                },
                headers={"Content-Type": "application/json"}
            )
            print(f"MCP Initialize Response: {response.text}")
        except Exception as e:
            print(f"MCP test error: {e}")
        
        print("\n✅ HF Space is accessible!")

if __name__ == "__main__":
    asyncio.run(test_hf_mcp())
