# Connecting to the PagerDuty MCP Server

This guide explains different ways to connect to and use the PagerDuty MCP server running as an HTTP/SSE service.

## 1. Docker Container Setup (Recommended)

The PagerDuty MCP server is configured to run as an HTTP/SSE service in Docker, making it accessible over the network.

### Prerequisites
- Docker and Docker Compose installed
- A valid PagerDuty API key

### Quick Start
1. **Set up your environment**:
   ```bash
   echo "PAGERDUTY_API_KEY=your_pagerduty_api_key_here" > .env
   ```

2. **Start the MCP server**:
   ```bash
   docker-compose up -d pagerduty-mcp-server
   ```
   
   The server will be available at: `http://localhost:3001/sse`

3. **Verify the server is running**:
   ```bash
   curl -I http://localhost:3001/sse
   ```

## 2. VS Code MCP Extension Connection

### Configuration
The `.vscode/mcp.json` file is configured to connect to your HTTP/SSE MCP server:

```json
{
    "servers": {
        "pagerduty-mcp-server": {
            "url": "http://localhost:3001/sse"
        }
    }
}
```

### Setup Steps
1. Ensure the Docker container is running (see section 1)
2. Install the MCP extension in VS Code
3. The extension should automatically detect and connect to the server at the configured URL
4. You can now use PagerDuty tools in VS Code through the MCP interface

## 3. Direct Docker Commands

### Build and Run
```bash
# Build the image
docker build -f docker/Dockerfile.mcp -t pagerduty-agent-mcp .

# Run the container with SSE endpoint
docker run -d \
  -p 3001:3000 \
  -e PAGERDUTY_API_KEY="your_api_key_here" \
  -e PAGERDUTY_API_URL="https://api.pagerduty.com" \
  -e MCP_HOST="0.0.0.0" \
  -e MCP_PORT="3000" \
  pagerduty-agent-mcp
```

## 4. Local Development (HTTP/SSE Mode)

### Running Locally with SSE Transport
```bash
# Install dependencies
poetry install

# Set environment variables
export PAGERDUTY_API_KEY="your_api_key_here"
export PAGERDUTY_API_URL="https://api.pagerduty.com"
export MCP_HOST="localhost"
export MCP_PORT="3000"

# Run the HTTP/SSE server
poetry run python -m agent_pagerduty.protocol_bindings.mcp_server.pagerduty_mcp.http_server
```

The server will be available at: `http://localhost:3000/sse`

## 5. Connecting from Other MCP Clients

### Claude Desktop (HTTP/SSE Connection)
Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "pagerduty": {
      "url": "http://localhost:3001/sse"
    }
  }
}
```

### Python MCP Client (HTTP/SSE)
```python
import asyncio
from fastmcp import Client

async def connect_to_pagerduty_mcp():
    # Connect via SSE to the HTTP server
    async with Client("http://localhost:3001/sse") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools])
        
        # Call a tool (example)
        result = await client.call_tool("get_incidents", {})
        print("Incidents:", result.content)

# Run the client
asyncio.run(connect_to_pagerduty_mcp())
```

### Python MCP Client (Alternative with explicit SSE transport)
```python
import asyncio
from fastmcp import Client

async def connect_to_pagerduty_mcp_explicit():
    # Connect via explicit SSE transport
    async with Client(
        transport="sse",
        host="localhost", 
        port=3001
    ) as client:
        # Initialize and use the client
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools])

# Run the client
asyncio.run(connect_to_pagerduty_mcp_explicit())
```

## 6. Testing the Connection

### Health Check
```bash
# Test if the server is responding
curl -v http://localhost:3001/sse

# You should see SSE headers in the response
```

### Using HTTPie (if installed)
```bash
# Install httpie if needed: pip install httpie
http GET localhost:3001/sse
```

### Browser Test
Open `http://localhost:3001/sse` in your browser. You should see an SSE stream connection.

## Available Tools

Once connected, you'll have access to these PagerDuty tools:

- **get_incidents**: List incidents
- **create_incident**: Create a new incident
- **update_incident**: Update an existing incident
- **resolve_incident**: Resolve an incident
- **acknowledge_incident**: Acknowledge an incident
- **get_services**: List services
- **create_service**: Create a new service
- **update_service**: Update an existing service
- **get_users**: List users
- **get_schedules**: List schedules
- **get_oncalls**: List on-call information

## Environment Variables

Required:
- `PAGERDUTY_API_KEY`: Your PagerDuty API key

Optional:
- `PAGERDUTY_API_URL`: PagerDuty API URL (defaults to https://api.pagerduty.com)

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure your `PAGERDUTY_API_KEY` is valid and has the necessary permissions
2. **Connection Refused**: Check that the server is running on the expected port
3. **Module Not Found**: Ensure dependencies are installed with `poetry install`
4. **Permission Denied**: Verify your API key has access to the PagerDuty resources you're trying to access

### Debugging

Enable debug logging by setting:
```bash
export PYTHONPATH=/path/to/project
export MCP_LOG_LEVEL=DEBUG
```

### Logs
- Docker logs: `docker-compose logs pagerduty-mcp-server`
- Local execution: Check console output for any error messages
