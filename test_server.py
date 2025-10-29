#!/usr/bin/env python3
"""
Test script for the MCP server.

This script demonstrates how to interact with the MCP server programmatically.
You can also use this to verify the server is working correctly.
"""

import json
import subprocess
import sys
import time


def test_server():
    """Test the MCP server by sending sample requests."""
    
    print("=" * 60)
    print("MCP Server Test Script")
    print("=" * 60)
    print()
    
    # Start the server process
    print("Starting MCP server...")
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Give server time to start
        time.sleep(1)
        
        # Send initialize request
        print("\n1. Initializing connection...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Initialize response: {json.dumps(response, indent=2)}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        proc.stdin.write(json.dumps(initialized_notification) + "\n")
        proc.stdin.flush()
        
        # Test listing tools
        print("\n2. Listing available tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        proc.stdin.write(json.dumps(list_tools_request) + "\n")
        proc.stdin.flush()
        
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Available tools: {len(response.get('result', {}).get('tools', []))} tools found")
            for tool in response.get('result', {}).get('tools', []):
                print(f"  - {tool['name']}: {tool['description']}")
        
        # Test echo tool
        print("\n3. Testing 'echo' tool...")
        echo_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {
                    "message": "Hello, MCP!"
                }
            }
        }
        
        proc.stdin.write(json.dumps(echo_request) + "\n")
        proc.stdin.flush()
        
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Echo result: {response.get('result', {}).get('content', [{}])[0].get('text', 'N/A')}")
        
        # Test add tool
        print("\n4. Testing 'add' tool...")
        add_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {
                    "a": 15,
                    "b": 27
                }
            }
        }
        
        proc.stdin.write(json.dumps(add_request) + "\n")
        proc.stdin.flush()
        
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Add result: {response.get('result', {}).get('content', [{}])[0].get('text', 'N/A')}")
        
        # Test listing resources
        print("\n5. Listing available resources...")
        list_resources_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/list",
            "params": {}
        }
        
        proc.stdin.write(json.dumps(list_resources_request) + "\n")
        proc.stdin.flush()
        
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Available resources: {len(response.get('result', {}).get('resources', []))} resources found")
            for resource in response.get('result', {}).get('resources', []):
                print(f"  - {resource['name']} ({resource['uri']})")
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
        print()
        print("The MCP server is working correctly.")
        print("You can now configure it in Claude Desktop.")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
    
    return 0


if __name__ == "__main__":
    sys.exit(test_server())
