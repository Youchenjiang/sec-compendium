#!/usr/bin/env python3
"""Minimal live MCP client probe (stdio transport).

Connects to an MCP server over stdio, performs the full session lifecycle
(initialize -> tools/list), and optionally calls one tool, printing the
raw result as JSON so it can be captured as evidence.

This is the executable counterpart of the wiring policy in
``.agent/mcp/README.md``: it proves a registered server is actually
reachable and callable, not just installable.

Usage:
  python mcp_probe.py --cmd <server-exe> [--arg ...] \
      [--path-prepend <dir>] [--cwd <dir>] \
      [--call <tool>] [--arguments '<json>'] [--out <file>]

Exit code 0 only if the session initialized and (when requested) the tool
call returned without a protocol error.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_lines: list[str] = []


def emit(section: str, payload: object) -> None:
    line = f"### {section}"
    print(line)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    print()
    _lines.append(line)
    _lines.append(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    _lines.append("")


async def run(args: argparse.Namespace) -> int:
    env = dict(os.environ)
    if args.path_prepend:
        env["PATH"] = os.path.abspath(args.path_prepend) + os.pathsep + env.get("PATH", "")
    if args.metrics_off:
        env["SEMGREP_SEND_METRICS"] = "off"

    params = StdioServerParameters(
        command=args.cmd,
        args=args.arg or [],
        env=env,
        cwd=args.cwd,
    )

    ok = True
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        init = await session.initialize()
        emit(
            "initialize",
            {
                "serverInfo": init.serverInfo.model_dump() if init.serverInfo else None,
                "protocolVersion": init.protocolVersion,
                "capabilities": init.capabilities.model_dump(),
            },
        )

        tools = await session.list_tools()
        emit(
            "tools/list",
            {
                "count": len(tools.tools),
                "tools": [
                    {"name": t.name, "description": (t.description or "").strip()}
                    for t in tools.tools
                ],
            },
        )

        if args.call:
            arguments = json.loads(args.arguments) if args.arguments else {}
            emit("tools/call.request", {"name": args.call, "arguments": arguments})
            result = await session.call_tool(args.call, arguments)
            emit(
                "tools/call.result",
                {
                    "isError": result.isError,
                    "structuredContent": result.structuredContent,
                    "content": [c.model_dump() for c in result.content],
                },
            )
            if result.isError:
                ok = False

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(_lines) + "\n")
    return 0 if ok else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Live MCP stdio client probe")
    p.add_argument("--cmd", required=True, help="server executable")
    p.add_argument("--arg", action="append", help="server argument (repeatable)")
    p.add_argument("--path-prepend", help="dir to prepend to PATH for the child")
    p.add_argument("--cwd", help="child working directory")
    p.add_argument("--call", help="tool name to call after listing")
    p.add_argument("--arguments", help="JSON object of tool arguments")
    p.add_argument("--metrics-off", action="store_true", help="set SEMGREP_SEND_METRICS=off for the child")
    p.add_argument("--out", help="write the captured evidence to this file")
    args = p.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
