# Docker Configuration for PagerDuty Agent

This directory contains Docker configurations for running the PagerDuty agent with different protocol bindings.

## Available Docker Files

### 1. Dockerfile.a2a
Builds a container for the A2A (Agent-to-Agent) protocol server.

**Usage:**
```bash
# Build the image
docker build -f docker/Dockerfile.a2a -t pagerduty-agent-a2a .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e PAGERDUTY_API_KEY="your_api_key_here" \
  -e PAGERDUTY_API_URL="https://api.pagerduty.com" \
  pagerduty-agent-a2a
```

### 2. Dockerfile.mcp
Builds a container for the MCP (Model Context Protocol) server with HTTP/SSE transport.

**Usage:**
```bash
# Build the image
docker build -f docker/Dockerfile.mcp -t pagerduty-agent-mcp .

# Run the container
docker run -d \
  -p 3001:3000 \
  -e PAGERDUTY_API_KEY="your_api_key_here" \
  -e PAGERDUTY_API_URL="https://api.pagerduty.com" \
  -e MCP_HOST="0.0.0.0" \
  -e MCP_PORT="3000" \
  pagerduty-agent-mcp

# The server will be available at: http://localhost:3001/sse
```

## Docker Compose

For easier management, use the provided `docker-compose.yml` file:

### Setup
1. Create a `.env` file in the project root:
```bash
PAGERDUTY_API_KEY=your_api_key_here
PAGERDUTY_API_URL=https://api.pagerduty.com
```

2. Run both services:
```bash
docker-compose up -d
```

3. Run only the MCP server:
```bash
docker-compose up -d pagerduty-mcp-server
```

4. Run only the A2A server:
```bash
docker-compose up -d pagerduty-a2a-server
```

## Environment Variables

Both containers require the following environment variables:

- `PAGERDUTY_API_KEY`: Your PagerDuty API key (required)
- `PAGERDUTY_API_URL`: PagerDuty API URL (optional, defaults to https://api.pagerduty.com)

## Ports

- **A2A Server**: Exposed on port 8000
- **MCP Server**: Exposed on port 3001 (mapped from container port 3000)
  - HTTP/SSE endpoint: `http://localhost:3001/sse`

## Connection Methods

### MCP Server HTTP/SSE Connection
The MCP server runs with SSE (Server-Sent Events) transport, making it accessible via HTTP:

- **Endpoint**: `http://localhost:3001/sse`
- **Protocol**: HTTP with SSE for real-time communication
- **Client Libraries**: Compatible with FastMCP clients and VS Code MCP extension

### A2A Server Connection
The A2A server provides traditional HTTP API endpoints on port 8000.

## Security Features

Both Dockerfiles include:
- Non-root user execution for enhanced security
- Proper file ownership and permissions
- Environment variable handling without exposing sensitive data in the image layers

## Available Tools (MCP Server)

The MCP server provides the following tools for PagerDuty management:

- **Incidents**: Create, list, update, acknowledge, and resolve incidents
- **Services**: List, create, and update services  
- **Users**: List users
- **Schedules**: List schedules
- **On-calls**: List on-call information

## Development

For development purposes, you can mount the source code as a volume:

```bash
docker run -d \
  -p 3000:3000 \
  -e PAGERDUTY_API_KEY="your_api_key_here" \
  -v $(pwd):/app \
  pagerduty-agent-mcp
```
