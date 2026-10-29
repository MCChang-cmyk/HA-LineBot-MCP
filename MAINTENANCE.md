# Maintained fork: 1.0.2

Original project: kukuxx/HA-LineBot-MCP. Apache-2.0 license retained.

Modified dependency pins to match Home Assistant Core 2026.10.3:
MCP 1.28.1, AnyIO 4.14.2. Other Core versions are not validated.
Updated repository links and declared minimum Core version in manifest and HACS metadata.
Domain, config entry keys, webhook routes and service names remain unchanged.

## Validation

Run `python -m pip install -r requirements-test.txt` then `python -m pytest -q`.
Tests use the real MCP SDK with minimal Home Assistant stubs and a mocked LINE client.
They cover in-memory protocol initialization, listing all three tools, successful push,
reply and quota calls, unknown bot failure, and the official server's ClientRequestType interface.
Local tests passed on Python 3.12. CI targets Python 3.14; CI has not run yet.
This is not a full Home Assistant Core startup/coexistence test.
No live LINE messages were sent. Webhook reception, automatic replies, SSE HTTP transport,
and the TV Box environment still require device validation.

## Installation and rollback

Back up Home Assistant and download the backup to another device first.
Back up `/config/custom_components/linebot_mcp` separately outside custom_components.
Keep existing integration configuration and LINE credentials.
The component ZIP contains only `custom_components/linebot_mcp/`; extract into `/config`
to replace the existing component files, then fully restart Home Assistant.
Check official MCP Server setup, LINE push/reply, webhook reception, and SSE connectivity.
If dependency/import errors persist, collect full logs; do not delete dependencies manually.
Restoring the old component restores its old conflicting package requirements too.
For complete rollback, restore the Home Assistant backup using its normal restore procedure.
Future HACS updates from the original repository can overwrite these fixes.
Switch HACS to this fork before relying on its updates; avoid installing both copies.
