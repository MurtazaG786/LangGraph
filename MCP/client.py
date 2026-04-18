import os
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_file):
        self.server_file = server_file
        self.session = None
        self._exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[self.server_file],
            env=os.environ.copy(),
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(_stdio, _write)
        )
        await self.session.initialize()

    async def list_tools(self):
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, name, arguments):
        result = await self.session.call_tool(name, arguments)
        text_parts = [item.text for item in result.content if hasattr(item, "text")]
        return "\n".join(text_parts) if text_parts else str(result)

    async def close(self):
        await self._exit_stack.aclose()
        self.session = None