#!/usr/bin/env python3
"""Test client for the OpenPIV MCP server on Hugging Face Spaces using HTTP streamable transport."""

import asyncio
import httpx
import json

async def test_hf_mcp_http():
    """Test the MCP server on HF Spaces using HTTP streamable transport."""
    base_url = "https://alexliberzon-openpiv-mcp.hf.space"
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # Step 1: Initialize session via POST to /mcp
        print("Step 1: Initializing MCP session...")
        response = await client.post(
            f"{base_url}/mcp",
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"}
                },
                "id": 1
            }
        )
        print(f"  Status: {response.status_code}")
        print(f"  Headers: {dict(response.headers)}")
        
        # Get session ID from header
        session_id = response.headers.get("mcp-session-id")
        print(f"  Session ID: {session_id}")
        
        if response.text:
            print(f"  Response body: {response.text[:500]}")
        
        # Step 2: List tools using the session
        if session_id:
            print("\nStep 2: Listing tools...")
            response = await client.post(
                f"{base_url}/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Mcp-Session-Id": session_id
                },
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 2
                }
            )
            print(f"  Status: {response.status_code}")
            if response.text:
                print(f"  Response: {response.text[:1000]}")
            else:
                # Try SSE stream
                print("  Checking SSE stream...")
        
        print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_hf_mcp_http())
