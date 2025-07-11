#!/usr/bin/env python3
"""
PagerDuty MCP HTTP Server

This server provides a Model Context Protocol (MCP) interface over HTTP/SSE to the PagerDuty API,
allowing large language models and AI assistants to manage PagerDuty resources remotely.
"""
import logging
import os
from dotenv import load_dotenv
from fastmcp import FastMCP

from agent_pagerduty.protocol_bindings.mcp_server.pagerduty_mcp.tools import (
    incidents,
    services,
    users,
    schedules,
    oncalls,
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("PagerDuty MCP Server")

# Register incident tools
mcp.tool()(incidents.get_incidents)
mcp.tool()(incidents.create_incident)
mcp.tool()(incidents.update_incident)
mcp.tool()(incidents.resolve_incident)
mcp.tool()(incidents.acknowledge_incident)
mcp.tool()(incidents.get_incident)

# Register service tools
mcp.tool()(services.get_services)
mcp.tool()(services.create_service)
mcp.tool()(services.update_service)

# Register user tools
mcp.tool()(users.get_users)

# Register schedule tools
mcp.tool()(schedules.get_schedules)

# Register oncall tools
mcp.tool()(oncalls.get_oncalls)

# Start server when run directly
if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "3000"))
    
    # Run the server with SSE transport for HTTP connectivity
    mcp.run(transport="sse", host=host, port=port)
