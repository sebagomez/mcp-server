# mcp-server
Tests for local MCP server

## Setup

Initialize if you don't have a package.json yet

> npm init -y

Runtime dep

> npm install @modelcontextprotocol/sdk

Dev deps for TS and Node types

> npm install -D typescript @types/node

Optional: run TS directly

> npm install -D tsx

Claude config

```json
{
  "mcpServers": {
    "hello-server": {
      "command": "npx",
      "args": [
        "tsx",
        "d:\\dev\\seba\\mcp-server\\mcp.ts"
      ]
    }
  }
}
```