#!/usr/bin/env python3
"""
Test script for HuggingFace Space MCP Server.

Usage:
    python test_hf_mcp.py
"""

import urllib.request
import urllib.error
import json
import sys


def make_request(url, data=None, follow_redirects=False):
    """Make HTTP request."""
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")

    if data:
        req.data = json.dumps(data).encode("utf-8")

    try:
        # Use a redirect handler that doesn't follow automatically
        import http.cookiejar

        cj = http.cookiejar.CookieJar()

        if follow_redirects:
            # Use default opener that follows redirects
            opener = urllib.request.build_opener()
        else:
            # Use opener that doesn't follow redirects
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())

        with opener.open(req) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        return 0, str(e)


def test_hf_space():
    """Test the HF Space MCP server."""
    base_url = "https://alexliberzon-openpiv-mcp.hf.space"

    print("=" * 60)
    print("Testing HF Space MCP Server")
    print("=" * 60)

    # Test health
    print("\n1. Testing health endpoint...")
    status, body = make_request(f"{base_url}/health")
    print(f"   Status: {status}")
    print(f"   Body: {body}")

    # Test root
    print("\n2. Testing root endpoint...")
    status, body = make_request(f"{base_url}/")
    print(f"   Status: {status}")
    print(f"   Body: {body}")

    # Test MCP initialize without redirect following
    print("\n3. Testing MCP /mcp (no redirect follow)...")
    status, body = make_request(
        f"{base_url}/mcp",
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"},
            },
        },
    )
    print(f"   Status: {status}")
    print(f"   Body: {body[:200] if body else 'empty'}...")

    # Test MCP with redirect following
    print("\n4. Testing MCP /mcp/ (with redirect follow)...")
    status, body = make_request(
        f"{base_url}/mcp/",
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"},
            },
        },
        follow_redirects=True,
    )
    print(f"   Status: {status}")
    print(f"   Body: {body[:200] if body else 'empty'}...")

    print("\n" + "=" * 60)
    print("Test complete")
    print("=" * 60)


if __name__ == "__main__":
    test_hf_space()
