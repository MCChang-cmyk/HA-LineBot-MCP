"""Exercise real MCP SDK with minimal Home Assistant stubs; no LINE network calls."""
import ast
import importlib.util
import json
from pathlib import Path
import sys
import types
from unittest.mock import AsyncMock, Mock

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'custom_components' / 'linebot_mcp'


def load_server():
    # Load only the server and constants, without bootstrapping Home Assistant.
    for name, path in [('compat_linebot', PACKAGE), ('compat_linebot.mcp_core', PACKAGE / 'mcp_core')]:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module
    for name in ['homeassistant', 'homeassistant.core', 'homeassistant.exceptions']:
        sys.modules[name] = types.ModuleType(name)
    sys.modules['homeassistant.core'].HomeAssistant = object
    sys.modules['homeassistant.exceptions'].HomeAssistantError = RuntimeError
    constants = types.ModuleType('compat_linebot.const')
    for node in ast.parse((PACKAGE / 'const.py').read_text()).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, (ast.Constant, ast.JoinedStr)):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    setattr(constants, target.id, eval(compile(ast.Expression(node.value), '<constants>', 'eval'), {}, vars(constants)))
    sys.modules['compat_linebot.const'] = constants
    for name, path in [('compat_linebot.mcp_core.server', PACKAGE / 'mcp_core/server.py')]:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module, sys.modules['compat_linebot.const']


@pytest.mark.asyncio
async def test_real_sdk_initialize_list_and_call_tools():
    server_module, const = load_server()
    client = types.SimpleNamespace(push_message=AsyncMock(), reply_message=AsyncMock())
    hass = types.SimpleNamespace(
        data={const.DOMAIN: {const.SERVICE_MANAGER: types.SimpleNamespace(get_bot_client={'@test': client})}},
        bus=types.SimpleNamespace(async_fire=Mock()),
        states=types.SimpleNamespace(get=Mock(return_value=types.SimpleNamespace(attributes={'total_quota': 200, 'used_quota': 3}))),
    )
    server = await server_module.MCPServerManager(hass).get_server()
    async with create_connected_server_and_client_session(server) as session:
        listed = await session.list_tools()
        assert len(listed.tools) == 3
        message = [{'type': 'text', 'text': 'test'}]
        push = await session.call_tool(const.MCP_TOOL_PUSH_MESSAGE, {'botID': '@test', 'to': 'U' + 'a' * 32, 'messages': message})
        assert not push.isError
        client.push_message.assert_awaited_once_with(to='U' + 'a' * 32, messages=message)
        reply = await session.call_tool(const.MCP_TOOL_REPLY_MESSAGE, {'botID': '@test', 'reply_token': 'token', 'messages': message})
        assert not reply.isError
        client.reply_message.assert_awaited_once_with(reply_token='token', messages=message)
        quota = await session.call_tool(const.MCP_TOOL_GET_QUOTA_INFO, {'botID': '@test'})
        assert not quota.isError
        assert '200' in quota.content[0].text
        invalid = await session.call_tool(const.MCP_TOOL_PUSH_MESSAGE, {'botID': '@missing', 'to': 'U' + 'a' * 32, 'messages': message})
        assert invalid.isError


def test_official_server_required_interface_exists():
    from mcp import types as mcp_types
    from typing import get_args
    assert get_args(mcp_types.ClientRequestType)
    manifest = json.loads((PACKAGE / 'manifest.json').read_text())
    from importlib.metadata import version
    for package in ['mcp', 'anyio']:
        assert f'{package}=={version(package)}' in manifest['requirements']
