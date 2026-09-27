import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_bus
import collab_mcp
import collab_protocol as protocol


def make_venv(root: Path, name: str, script: str) -> Path:
    """Create both a Windows-style and a POSIX-style venv layout under ``root``."""
    venv = root / ".agent" / "mcp" / ".verify" / name
    for sub in ("Scripts", "bin"):
        binary_dir = venv / sub
        binary_dir.mkdir(parents=True, exist_ok=True)
        (binary_dir / "python").touch()
        (binary_dir / f"{script}").touch()
        (binary_dir / f"python.exe").touch()
        (binary_dir / f"{script}.exe").touch()
    return venv


class CollabMcpTests(unittest.TestCase):
    def test_real_registry_lists_registered_servers_with_runners(self) -> None:
        registry = collab_mcp.load_registry()
        servers = {entry["name"]: entry for entry in registry["servers"]}
        self.assertIn("semgrep", servers)
        self.assertIn("cve-mcp-server", servers)
        for name, entry in servers.items():
            runner = entry.get("runner") or {}
            self.assertTrue(runner.get("venv"), f"{name} is missing runner.venv")
            self.assertTrue(runner.get("script"), f"{name} is missing runner.script")

    def test_get_server_raises_for_unknown_name_and_names_known_ones(self) -> None:
        registry = {"servers": [{"name": "alpha"}, {"name": "beta"}]}
        with self.assertRaises(ValueError) as ctx:
            collab_mcp.get_server(registry, "gamma")
        message = str(ctx.exception)
        self.assertIn("unknown MCP server 'gamma'", message)
        self.assertIn("alpha", message)
        self.assertIn("beta", message)

    def test_get_server_returns_matching_entry(self) -> None:
        registry = {"servers": [{"name": "alpha"}, {"name": "beta"}]}
        self.assertEqual(collab_mcp.get_server(registry, "beta"), {"name": "beta"})

    def test_resolve_runner_builds_command_args_and_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_venv(root, "semgrep178", "semgrep")
            entry = {
                "name": "semgrep",
                "runner": {
                    "venv": ".agent/mcp/.verify/semgrep178",
                    "script": "semgrep",
                    "args": ["mcp", "-t", "stdio"],
                },
            }
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                runner = collab_mcp.resolve_runner(entry)
                self.assertIn("semgrep", Path(runner["command"]).name)
                self.assertIn("-t", runner["args"])
                self.assertIn("stdio", runner["args"])
                self.assertIn("python", Path(runner["python"]).name)
                self.assertTrue(Path(runner["path_prepend"]).is_dir())

    def test_resolve_runner_resolves_relative_env_paths_against_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_venv(root, "cve-mcp", "cve-mcp")
            entry = {
                "name": "cve-mcp-server",
                "runner": {
                    "venv": ".agent/mcp/.verify/cve-mcp",
                    "script": "cve-mcp",
                    "args": [],
                    "env": {"CACHE_DB_PATH": ".agent/mcp/.verify/cve-cache.db"},
                },
            }
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                runner = collab_mcp.resolve_runner(entry)

        self.assertEqual(
            Path(runner["env"]["CACHE_DB_PATH"]), root / ".agent/mcp/.verify/cve-cache.db"
        )

    def test_resolve_runner_reports_missing_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "name": "ghost",
                "docs": "servers/ghost.md",
                "runner": {"venv": ".agent/mcp/.verify/ghost", "script": "ghost", "args": []},
            }
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                with self.assertRaises(ValueError) as ctx:
                    collab_mcp.resolve_runner(entry)
        self.assertIn("runtime not provisioned", str(ctx.exception))
        self.assertIn("servers/ghost.md", str(ctx.exception))

    def test_resolve_runner_reports_missing_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            venv = root / ".agent" / "mcp" / ".verify" / "half"
            (venv / "Scripts").mkdir(parents=True)
            (venv / "Scripts" / "python.exe").touch()
            entry = {
                "name": "half",
                "runner": {"venv": ".agent/mcp/.verify/half", "script": "half", "args": []},
            }
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                with self.assertRaises(ValueError) as ctx:
                    collab_mcp.resolve_runner(entry)
        self.assertIn("not found under", str(ctx.exception))

    def test_resolve_runner_requires_runner_block(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            collab_mcp.resolve_runner({"name": "bare"})
        self.assertIn("no 'runner' block", str(ctx.exception))

    def test_parse_sections_decodes_json_and_keeps_non_json_text(self) -> None:
        stdout = (
            "### initialize\n"
            '{"serverInfo": {"name": "cve-mcp", "version": "1.30.0"}}\n\n'
            "### tools/call.result\n"
            "plain text failure\n"
        )
        sections = collab_mcp._parse_sections(stdout)
        self.assertEqual(sections["initialize"]["serverInfo"]["name"], "cve-mcp")
        self.assertEqual(sections["tools/call.result"], "plain text failure")

    def test_parse_sections_ignores_leading_noise(self) -> None:
        sections = collab_mcp._parse_sections("### tools/list\n{\"count\": 7}\n")
        self.assertEqual(sections["tools/list"]["count"], 7)

    def test_add_subcommands_parses_call_invocation(self) -> None:
        parser = argparse.ArgumentParser()
        collab_mcp.add_subcommands(parser)
        args = parser.parse_args(
            ["call", "--server", "semgrep", "--tool", "lookup", "--args", '{"a": 1}']
        )
        self.assertEqual(args.server, "semgrep")
        self.assertEqual(args.tool, "lookup")
        self.assertEqual(json.loads(args.args), {"a": 1})
        self.assertIs(args.func, collab_mcp.command_call)

    def test_collab_bus_exposes_mcp_subcommand(self) -> None:
        args = collab_bus.build_parser().parse_args(["mcp", "list"])
        self.assertIs(args.func, collab_mcp.command_list)
        args = collab_bus.build_parser().parse_args(
            ["mcp", "call", "--server", "semgrep", "--tool", "t"]
        )
        self.assertIs(args.func, collab_mcp.command_call)

    def test_command_list_is_offline_and_reports_registry_state(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exit_code = collab_mcp.command_list(argparse.Namespace())
        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("semgrep status=wired", output)
        self.assertIn("cve-mcp-server status=wired", output)
        self.assertIn("runtime=ready", output)

    def test_run_session_rejects_missing_probe(self) -> None:
        registry = {"servers": []}
        missing = protocol.REPO_ROOT / ".agent" / "mcp" / "tools" / "definitely-missing.py"
        with patch.object(collab_mcp, "PROBE_PATH", missing):
            with self.assertRaises(ValueError) as ctx:
                collab_mcp.run_session(registry, "anything")
        self.assertIn("probe missing", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
