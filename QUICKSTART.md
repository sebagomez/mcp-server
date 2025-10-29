# Quick Start Guide

This guide will help you get the MCP server running with Claude Desktop in just a few minutes.

## Step 1: Install Dependencies

```bash
cd mcp-server
pip3 install -r requirements.txt
```

## Step 2: Test the Server

Run the test script to verify everything works:

```bash
python3 test_server.py
```

You should see output indicating all tests passed successfully.

## Step 3: Configure Claude Desktop

### For macOS:

1. Find your current directory path:
```bash
pwd
```

2. Edit Claude's config file:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. Add this configuration (replace `/absolute/path/to/mcp-server` with your actual path):
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

### For Windows:

1. Find your current directory path in PowerShell:
```powershell
pwd
```

2. Edit Claude's config file:
```
notepad %APPDATA%\Claude\claude_desktop_config.json
```

3. Add this configuration (replace `C:\absolute\path\to\mcp-server` with your actual path):
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

## Step 4: Restart Claude Desktop

Completely quit and reopen Claude Desktop. The server should now be connected.

## Step 5: Test with Claude

Try these commands in Claude:
- "Use the echo tool to say hello"
- "Add 42 and 58 using the add tool"
- "What's my system information?"

## Troubleshooting

If the server doesn't appear:
1. Check Claude Desktop logs (Help → View Logs)
2. Verify the path in the config is absolute and correct
3. Make sure Python 3.10+ is installed: `python3 --version`
4. Ensure dependencies are installed: `pip3 list | grep mcp`

## Using a Virtual Environment (Recommended)

For better isolation:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then use the venv Python in your config:
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
