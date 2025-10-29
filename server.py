#!/usr/bin/env python3
"""
A simple MCP server for local testing with Claude.

This server provides basic tools and resources to demonstrate
MCP protocol capabilities.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
app = Server("test-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echoes back the provided message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="add",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_system_info",
            description="Returns basic system information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "echo":
            message = arguments.get("message")
            if not message:
                raise ValueError("message is required")
            
            return [TextContent(
                type="text",
                text=f"Echo: {message}"
            )]
        
        elif name == "add":
            a = arguments.get("a")
            b = arguments.get("b")
            
            if a is None or b is None:
                raise ValueError("Both a and b are required")
            
            result = float(a) + float(b)
            return [TextContent(
                type="text",
                text=f"The sum of {a} and {b} is {result}"
            )]
        
        elif name == "get_system_info":
            import platform
            import sys
            
            info = {
                "platform": platform.platform(),
                "python_version": sys.version,
                "architecture": platform.machine()
            }
            
            return [TextContent(
                type="text",
                text=f"System Information:\n" + "\n".join(f"{k}: {v}" for k, v in info.items())
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        raise


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="test://greeting",
            name="Greeting Message",
            mimeType="text/plain",
            description="A simple greeting message"
        ),
        Resource(
            uri="test://info",
            name="Server Info",
            mimeType="application/json",
            description="Information about this MCP server"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if uri == "test://greeting":
        return "Hello from the MCP test server!"
    
    elif uri == "test://info":
        import json
        info = {
            "name": "test-mcp-server",
            "version": "1.0.0",
            "description": "A simple MCP server for local testing with Claude",
            "capabilities": ["tools", "resources"]
        }
        return json.dumps(info, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Run the MCP server."""
    logger.info("Starting MCP test server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
