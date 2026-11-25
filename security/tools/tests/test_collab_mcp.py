import argparse
import contextlib
import io
import json
import os
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
import mcp_transports


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


class GateAuditTests(unittest.TestCase):
    def test_audit_record_omits_transport_when_it_is_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "gate.jsonl"
            collab_mcp.record_gate_decision(
                {"server": "x", "tool": None, "decision": "allow", "reason": "ok"},
                log_path=log,
            )
            record = json.loads(log.read_text(encoding="utf-8").strip())
            self.assertNotIn("transport", record)
            self.assertNotIn("node", record)


class CollabMcpTests(unittest.TestCase):
    def test_real_registry_gives_every_server_a_runnable_transport(self) -> None:
        registry = collab_mcp.load_registry()
        policy = mcp_transports.normalise_policy(registry)
        servers = {entry["name"]: entry for entry in registry["servers"]}
        self.assertIn("semgrep", servers)
        self.assertIn("cve-mcp-server", servers)
        for name, entry in servers.items():
            transport = mcp_transports.transport_for(entry, policy=policy)
            self.assertIn(transport, mcp_transports.NODE_TRANSPORTS)
            runner = entry.get("runner") or {}
            if transport == "stdio_local":
                self.assertTrue(runner.get("venv"), f"{name} is missing runner.venv")
                self.assertTrue(runner.get("script"), f"{name} is missing runner.script")
            else:
                # A node-bound server must describe both how to reach the node and
                # what to run there; planning is what validates the rest.
                self.assertTrue(
                    mcp_transports.node_block(entry), f"{name} needs a runner.node block"
                )
                self.assertIn("holder_class", entry.get("placement") or {})

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
        # The readiness token must match reality: a fresh clone has no venvs, and
        # this view has to keep telling the truth there too.
        registry = collab_mcp.load_registry()
        for entry in registry["servers"]:
            venv = protocol.REPO_ROOT / (entry.get("runner") or {}).get("venv", "")
            expected = "runtime=ready" if venv.exists() else "runtime=missing"
            with self.subTest(server=entry["name"]):
                self.assertIn(f"{entry['name']} status=", output)
                self.assertIn(expected, output)

    def test_real_registry_declares_placement_and_capabilities(self) -> None:
        """Every wired server must state where it runs and what it can do."""
        registry = collab_mcp.load_registry()
        for entry in registry["servers"]:
            with self.subTest(server=entry["name"]):
                self.assertTrue(entry.get("placement", {}).get("holder_class"))
                self.assertTrue(entry.get("placement", {}).get("rationale"))
                self.assertTrue(entry.get("capability_class"))
                self.assertNotIn("unclassified", collab_mcp.capability_classes(entry))

    def test_real_registry_authorization_defaults_to_deny(self) -> None:
        policy = collab_mcp.authorization_policy(collab_mcp.load_registry())
        self.assertEqual(policy["default_decision"], "deny")
        self.assertIn("command_exec", policy["applies_to_capabilities"])
        self.assertIn("write", policy["applies_to_capabilities"])
        self.assertIn("unclassified", policy["applies_to_capabilities"])
        self.assertEqual(policy["command_exec_allowlist"], [])

    def test_run_session_rejects_missing_probe(self) -> None:
        registry = {"servers": []}
        missing = protocol.REPO_ROOT / ".agent" / "mcp" / "tools" / "definitely-missing.py"
        with patch.object(collab_mcp, "PROBE_PATH", missing):
            with self.assertRaises(ValueError) as ctx:
                collab_mcp.run_session(registry, "anything")
        self.assertIn("probe missing", str(ctx.exception))


def gate_registry(allowlist: list[dict] | None = None) -> dict:
    """Registry fixture: one harmless server plus one command-capable server."""
    return {
        "servers": [
            {"name": "reader", "capability_class": ["read_only"]},
            {"name": "danger", "capability_class": ["command_exec"]},
            {"name": "mystery"},
        ],
        "authorization": {
            "policy_version": 1,
            "default_decision": "deny",
            "applies_to_capabilities": ["command_exec", "write", "unclassified"],
            "authorization_env": "MCP_AUTHORIZATION",
            "command_exec_allowlist": list(allowlist or []),
        },
    }


ALLOW_ENTRY = {
    "server": "danger",
    "tools": ["run_command"],
    "paths_allow": ["security/"],
    "deny_patterns": [r";\s*rm\b", r"\|\s*(sh|bash)\b"],
    "requires_authorization": True,
    "note": "fixture entry",
}


class McpAuthorizationGateTests(unittest.TestCase):
    def test_gate_allows_server_without_gated_capability(self) -> None:
        decision = collab_mcp.gate_decision(gate_registry(), "reader", "lookup", {})
        self.assertEqual(decision["decision"], "allow")
        self.assertIn("no gated capability", decision["reason"])

    def test_gate_denies_command_exec_without_allowlist_entry(self) -> None:
        decision = collab_mcp.gate_decision(gate_registry(), "danger", "run_command", {})
        self.assertEqual(decision["decision"], "deny")
        self.assertIn("command_exec_allowlist", decision["reason"])
        self.assertIn("default decision is deny", decision["reason"])

    def test_gate_treats_missing_capability_as_gated(self) -> None:
        decision = collab_mcp.gate_decision(gate_registry(), "mystery", "anything", {})
        self.assertEqual(decision["decision"], "deny")
        self.assertIn("unclassified", decision["gated_capabilities"])

    def test_gate_denies_tool_outside_the_allowlist(self) -> None:
        decision = collab_mcp.gate_decision(
            gate_registry([ALLOW_ENTRY]), "danger", "wipe_disk", {}
        )
        self.assertEqual(decision["decision"], "deny")
        self.assertIn("not allowlisted", decision["reason"])

    def test_gate_denies_path_argument_outside_the_allowlisted_scope(self) -> None:
        registry = gate_registry([ALLOW_ENTRY])
        allowed = collab_mcp.gate_decision(
            registry,
            "danger",
            "run_command",
            {"target": "security/tools/collab_mcp.py"},
            authorized_reason="triaging C04 finding",
            process_env={"MCP_AUTHORIZATION": "1"},
        )
        self.assertEqual(allowed["decision"], "allow")
        denied = collab_mcp.gate_decision(
            registry,
            "danger",
            "run_command",
            {"target": "C:/Windows/System32/cmd.exe"},
            authorized_reason="triaging C04 finding",
            process_env={"MCP_AUTHORIZATION": "1"},
        )
        self.assertEqual(denied["decision"], "deny")
        self.assertIn("outside the allowlisted scope", denied["reason"])

    def test_gate_denies_argument_matching_a_deny_pattern(self) -> None:
        decision = collab_mcp.gate_decision(
            gate_registry([ALLOW_ENTRY]),
            "danger",
            "run_command",
            {"cmd": "cat security/x ; rm -rf security"},
            authorized_reason="approved",
            process_env={"MCP_AUTHORIZATION": "1"},
        )
        self.assertEqual(decision["decision"], "deny")
        self.assertIn("deny pattern", decision["reason"])

    def test_gate_requires_reason_and_authorization_env(self) -> None:
        registry = gate_registry([ALLOW_ENTRY])
        no_reason = collab_mcp.gate_decision(
            registry, "danger", "run_command", {}, process_env={"MCP_AUTHORIZATION": "1"}
        )
        self.assertEqual(no_reason["decision"], "deny")
        self.assertIn("--authorized", no_reason["reason"])

        no_env = collab_mcp.gate_decision(
            registry, "danger", "run_command", {}, authorized_reason="approved", process_env={}
        )
        self.assertEqual(no_env["decision"], "deny")
        self.assertIn("MCP_AUTHORIZATION", no_env["reason"])

    def test_gate_denies_expired_allowlist_entry(self) -> None:
        expired = dict(ALLOW_ENTRY, expires="2000-01-01")
        decision = collab_mcp.gate_decision(
            gate_registry([expired]),
            "danger",
            "run_command",
            {},
            authorized_reason="approved",
            process_env={"MCP_AUTHORIZATION": "1"},
        )
        self.assertEqual(decision["decision"], "deny")
        self.assertIn("expired", decision["reason"])

    def test_enforce_gate_raises_on_denial(self) -> None:
        registry = gate_registry()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(collab_mcp, "GATE_LOG_PATH", Path(tmp) / "gate.jsonl"):
                with self.assertRaises(ValueError) as ctx:
                    collab_mcp.enforce_gate(registry, "danger", "run_command", {})
        self.assertIn("authorization gate denied", str(ctx.exception))

    def test_record_gate_decision_appends_an_audit_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "nested" / "mcp-gate.jsonl"
            collab_mcp.record_gate_decision(
                {
                    "server": "danger",
                    "tool": "run_command",
                    "capabilities": ["command_exec"],
                    "decision": "deny",
                    "reason": "no allowlist entry",
                },
                reason="why the operator asked",
                mode="dry-run",
                log_path=log,
            )
            record = json.loads(log.read_text(encoding="utf-8").strip())
        self.assertEqual(record["decision"], "deny")
        self.assertEqual(record["server"], "danger")
        self.assertEqual(record["mode"], "dry-run")
        self.assertEqual(record["authorized_reason"], "why the operator asked")
        self.assertIn("at", record)

    def test_command_gate_returns_zero_on_allow_and_two_on_deny(self) -> None:
        registry = gate_registry([ALLOW_ENTRY])
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(collab_mcp, "load_registry", return_value=registry), patch.object(
                collab_mcp, "GATE_LOG_PATH", Path(tmp) / "gate.jsonl"
            ):
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    allowed = collab_mcp.command_gate(
                        argparse.Namespace(
                            server="reader", tool="lookup", args="", authorized=""
                        )
                    )
                self.assertEqual(allowed, 0)
                self.assertIn('"decision": "allow"', buffer.getvalue())

                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    denied = collab_mcp.command_gate(
                        argparse.Namespace(
                            server="danger", tool="run_command", args="", authorized=""
                        )
                    )
                self.assertEqual(denied, 2)
                self.assertIn('"decision": "deny"', buffer.getvalue())

    def test_command_gate_reports_unknown_server_as_denied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(collab_mcp, "load_registry", return_value=gate_registry()), patch.object(
                collab_mcp, "GATE_LOG_PATH", Path(tmp) / "gate.jsonl"
            ):
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    code = collab_mcp.command_gate(
                        argparse.Namespace(server="ghost", tool="x", args="", authorized="")
                    )
        self.assertEqual(code, 2)
        self.assertIn("unknown MCP server", buffer.getvalue())


class McpSecretsTests(unittest.TestCase):
    def test_parse_secrets_env_handles_comments_quotes_and_export(self) -> None:
        parsed = collab_mcp.parse_secrets_env(
            "# comment\n\nNVD_API_KEY=abc123\nexport GITHUB_TOKEN='ghp_x'\n"
            'SHODAN_KEY="shodan$literal"\nnot-a-line\n'
        )
        self.assertEqual(parsed["NVD_API_KEY"], "abc123")
        self.assertEqual(parsed["GITHUB_TOKEN"], "ghp_x")
        self.assertEqual(parsed["SHODAN_KEY"], "shodan$literal")
        self.assertEqual(len(parsed), 3)

    def test_resolve_secret_env_only_returns_declared_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            secrets_file = Path(tmp) / "secrets.env"
            secrets_file.write_text(
                "DECLARED_KEY=value\nOTHER_SERVER_KEY=secret\n", encoding="utf-8"
            )
            entry = {
                "name": "gated",
                "secrets_binding": {"required": False, "env": ["DECLARED_KEY"]},
            }
            values, missing = collab_mcp.resolve_secret_env(
                entry, secrets_file=secrets_file, process_env={}
            )
        self.assertEqual(values, {"DECLARED_KEY": "value"})
        self.assertNotIn("OTHER_SERVER_KEY", values)
        self.assertEqual(missing, [])

    def test_resolve_secret_env_reports_missing_and_falls_back_to_process_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            secrets_file = Path(tmp) / "absent-secrets.env"
            entry = {
                "name": "gated",
                "secrets_binding": {"required": False, "env": ["FROM_ENV", "ABSENT"]},
            }
            values, missing = collab_mcp.resolve_secret_env(
                entry, secrets_file=secrets_file, process_env={"FROM_ENV": "set"}
            )
        self.assertEqual(values, {"FROM_ENV": "set"})
        self.assertEqual(missing, ["ABSENT"])

    def test_declared_secret_names_prefers_binding_over_legacy_block(self) -> None:
        entry = {
            "name": "legacy",
            "secrets_binding": {"env": ["NEW_NAME"]},
            "secrets": {"env": ["OLD_NAME (deprecated note)"]},
        }
        self.assertEqual(collab_mcp.declared_secret_names(entry), ["NEW_NAME"])

    def test_secrets_binding_reports_injection_mode(self) -> None:
        self.assertEqual(
            collab_mcp.secrets_binding({"name": "x"})["inject"], "none"
        )
        self.assertEqual(
            collab_mcp.secrets_binding(
                {"name": "x", "secrets_binding": {"env": ["T"]}}
            )["inject"],
            "host-env",
        )

    def test_command_secrets_prints_names_without_values(self) -> None:
        registry = {
            "servers": [
                {
                    "name": "gated",
                    "capability_class": ["read_only"],
                    "secrets_binding": {"required": True, "env": ["HITCON_MCP_TEST_TOKEN"]},
                }
            ]
        }
        with patch.object(collab_mcp, "load_registry", return_value=registry), patch.object(
            collab_mcp, "SECRETS_PATH", Path("definitely-absent-secrets.env")
        ), patch.dict(os.environ, {"HITCON_MCP_TEST_TOKEN": "super-secret-value"}, clear=False):
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = collab_mcp.command_secrets(argparse.Namespace(server="gated"))
        output = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("HITCON_MCP_TEST_TOKEN present", output)
        self.assertNotIn("super-secret-value", output)

    def test_run_session_requires_declared_secrets_when_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_venv(root, "gated", "gated")
            probe = root / "probe.py"
            probe.write_text("# probe\n", encoding="utf-8")
            registry = {
                "servers": [
                    {
                        "name": "gated",
                        "capability_class": ["read_only"],
                        "runner": {
                            "venv": ".agent/mcp/.verify/gated",
                            "script": "gated",
                            "args": [],
                        },
                        "secrets_binding": {
                            "required": True,
                            "env": ["HITCON_MCP_TEST_TOKEN_ABSENT"],
                        },
                    }
                ]
            }
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root), patch.object(
                collab_mcp, "PROBE_PATH", probe
            ), patch.object(
                collab_mcp, "SECRETS_PATH", root / "secrets.env"
            ), patch.object(
                collab_mcp, "GATE_LOG_PATH", root / "gate.jsonl"
            ), patch.dict(
                os.environ, {"HITCON_MCP_TEST_TOKEN_ABSENT": ""}, clear=False
            ):
                with self.assertRaises(ValueError) as ctx:
                    collab_mcp.run_session(registry, "gated")
        message = str(ctx.exception)
        self.assertIn("missing required secret env names", message)
        self.assertIn("HITCON_MCP_TEST_TOKEN_ABSENT", message)
        self.assertIn("secrets.env", message)


if __name__ == "__main__":
    unittest.main()
