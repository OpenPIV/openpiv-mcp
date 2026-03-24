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


def make_request(url, data=None):
    """Make HTTP request."""
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")

    if data:
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def test_hf_space():
    """Test the HF Space MCP server."""
    base_url = "https://alexliberzon-openpiv-mcp.hf.space"

    print("=" * 50)
    print("Testing HF Space MCP Server")
    print("=" * 50)

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

    # Test MCP initialize
    print("\n3. Testing MCP initialize (without trailing slash)...")
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
    print(f"   Body: {body[:200]}...")

    # Check if we got a redirect
    if status == 307:
        print(
            "\n   ⚠️ Got 307 redirect - the MCP server requires trailing slash handling"
        )

    print("\n" + "=" * 50)
    print("Test complete")
    print("=" * 50)


if __name__ == "__main__":
    test_hf_space()
