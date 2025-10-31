import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create MCP server
const server = new Server(
  {
    name: "hello-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {}, // This server provides tools
    },
  }
);

// Handler: List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "say_hello",
      description: "Returns a greeting with the provided name",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "The name to greet",
          },
        },
        required: ["name"],
      },
    },
  ],
}));

// Handler: Execute tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name: toolName, arguments: args } = request.params;

  if (toolName !== "say_hello") {
    throw new Error(`Unknown tool: ${toolName}`);
  }

  // Validate arguments
  if (!args || typeof args.name !== "string") {
    throw new Error("Missing or invalid 'name' argument");
  }

  const userName = args.name;
  
  return {
    content: [
      {
        type: "text",
        text: `Hello, ${userName}! Nice to meet you.`,
      },
    ],
  };
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Hello MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});