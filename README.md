# MCP Server - Python Implementation

A simple Model Context Protocol (MCP) server implementation in Python for local testing with Claude Desktop.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables AI assistants like Claude to securely connect to external data sources and tools. This server demonstrates how to build a basic MCP server in Python.

## Features

This MCP server provides:

### Tools
- **echo**: Echoes back any message you send
- **add**: Adds two numbers together
- **get_system_info**: Returns system information (platform, Python version, etc.)

### Resources
- **test://greeting**: A simple greeting message
- **test://info**: JSON information about the server

## Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/sebagomez/mcp-server.git
cd mcp-server
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing the Server

### Standalone Testing

You can test the server directly using the provided test script:

```bash
python3 test_server.py
```

This will:
- Start the server
- Test all available tools
- Display the results

### Integration with Claude Desktop

To use this server with Claude Desktop, you need to configure it in Claude's settings.

#### macOS Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "test-server": {
      "command": "python3",
      "args": [
        "/absolute/path/to/mcp-server/server.py"
      ]
    }
  }
}
```

#### Windows Configuration

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "test-server": {
      "command": "python",
      "args": [
        "C:\\absolute\\path\\to\\mcp-server\\server.py"
      ]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/mcp-server/` with the actual absolute path to your cloned repository.

If you're using a virtual environment, you should use the Python interpreter from that environment:

```json
{
  "mcpServers": {
    "test-server": {
      "command": "/absolute/path/to/mcp-server/venv/bin/python3",
      "args": [
        "/absolute/path/to/mcp-server/server.py"
      ]
    }
  }
}
```

#### After Configuration

1. Restart Claude Desktop completely (quit and reopen)
2. Look for the 🔌 icon in Claude's interface to see connected MCP servers
3. You can now ask Claude to use the tools, for example:
   - "Use the echo tool to say hello"
   - "Add 5 and 7 using the add tool"
   - "What's the system info?"

## Development

### Project Structure

```
mcp-server/
├── server.py           # Main MCP server implementation
├── test_server.py      # Test script for standalone testing
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore patterns
```

### Adding New Tools

To add a new tool, update the `list_tools()` and `call_tool()` functions in `server.py`:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="your_tool",
            description="Description of your tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "your_tool":
        param = arguments.get("param")
        # Your tool logic here
        return [TextContent(type="text", text=f"Result: {param}")]
    # ... rest of the function ...
```

### Adding New Resources

To add a new resource, update the `list_resources()` and `read_resource()` functions:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        # ... existing resources ...
        Resource(
            uri="test://your_resource",
            name="Your Resource",
            mimeType="text/plain",
            description="Description of your resource"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "test://your_resource":
        return "Your resource content"
    # ... rest of the function ...
```

## Troubleshooting

### Server Not Appearing in Claude

1. Make sure you've completely quit and restarted Claude Desktop
2. Verify the paths in your `claude_desktop_config.json` are absolute and correct
3. Check that Python and dependencies are installed correctly
4. Look at Claude's logs (Help → View Logs) for error messages

### Import Errors

If you get import errors, make sure you've:
1. Activated your virtual environment (if using one)
2. Installed all requirements: `pip install -r requirements.txt`
3. Are using Python 3.10 or higher

### Tool Not Working

Check the Claude Desktop logs for detailed error messages. The server logs to stderr which Claude captures.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/download)

## License

This is a test/example project for learning MCP server development.
