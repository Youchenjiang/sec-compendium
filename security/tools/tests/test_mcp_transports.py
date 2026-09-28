"""Tests for node transports: planning, quoting, secret boundaries and the vmrun bridge.

The vmrun round trip runs the *real* host bridge, the *real* guest bridge and a
faux ``vmrun`` (``fake_vmrun.py``), so the file-bridge protocol is exercised
end to end without VMware: only the guest-operations calls themselves are stubbed.
"""

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_DIR.parents[1]
MCP_TOOLS_DIR = REPO_ROOT / ".agent" / "mcp" / "tools"
for extra in (str(TOOLS_DIR), str(Path(__file__).resolve().parent), str(MCP_TOOLS_DIR)):
    if extra not in sys.path:
        sys.path.insert(0, extra)

import collab_mcp
import fake_vmrun
import mcp_transports

VMRUN_BRIDGE = REPO_ROOT / ".agent" / "mcp" / "tools" / "mcp_vmrun_bridge.py"
NODE_BRIDGE = REPO_ROOT / ".agent" / "mcp" / "tools" / "mcp_node_bridge.py"

ECHO_SERVER = '''
import json
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    message = json.loads(line)
    method = message.get("method")
    if method == "initialize":
        result = {"protocolVersion": "2025-06-18", "serverInfo": {"name": "echo-node", "version": "0"}}
    elif method == "tools/list":
        result = {"tools": [{"name": "ping", "description": "reply with pong"}]}
    else:
        result = {"content": [{"type": "text", "text": "pong"}]}
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": message.get("id"), "result": result}) + "\\n")
    sys.stdout.flush()
'''


def fake_which(mapping: dict):
    """A ``shutil.which`` stand-in backed by an explicit binary map."""

    def _which(name: str):
        return mapping.get(name)

    return _which


def make_probe_env(root: Path, name: str = "probe") -> Path:
    """Create a venv-shaped directory with an interpreter in both layouts."""
    venv = root / ".agent" / "mcp" / ".verify" / name
    for sub in ("Scripts", "bin"):
        directory = venv / sub
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "python.exe").touch()
        (directory / "python").touch()
    return venv


def ssh_entry(**ssh_overrides) -> dict:
    ssh = {"host": {"secret": "KALI_HOST"}, "user": {"secret": "KALI_USER"}}
    ssh.update(ssh_overrides)
    return {
        "name": "kali-scanner",
        "placement": {"holder_class": "kali"},
        "capability_class": ["analysis"],
        "runner": {
            "node": {
                "transport": "ssh",
                "ssh": ssh,
                "exec": {
                    "command": "/opt/mcp/bin/server",
                    "args": ["--mode", "stdio", "--label", "two words"],
                    "cwd": "/opt/mcp",
                    "env": {"MCP_LABEL": "a b"},
                    "path_prepend": "/opt/mcp/bin",
                },
            }
        },
    }


def container_entry(**container_overrides) -> dict:
    container = {
        "image": "python:3.12-alpine",
        "mounts": [{"host": ".agent/mcp/.verify", "container": "/work"}],
        "workdir": "/work",
    }
    container.update(container_overrides)
    return {
        "name": "container-scanner",
        "placement": {"holder_class": "container"},
        "capability_class": ["command_exec"],
        "runner": {
            "node": {
                "transport": "container",
                "container": container,
                "exec": {"command": "python3", "args": ["/work/scan.py", "--stdio"]},
            }
        },
    }


class TransportSelectionTests(unittest.TestCase):
    def test_holder_class_selects_the_transport(self) -> None:
        cases = {
            "host_gateway": "stdio_local",
            "kali": "ssh",
            "flare_vm": "vmrun_guest",
            "container": "container",
        }
        for holder, expected in cases.items():
            entry = {"name": "x", "placement": {"holder_class": holder}}
            self.assertEqual(
                mcp_transports.transport_for(entry), expected, f"holder {holder} mapped wrong"
            )

    def test_explicit_runner_transport_overrides_the_holder_default(self) -> None:
        entry = {
            "name": "x",
            "placement": {"holder_class": "kali"},
            "runner": {"node": {"transport": "container"}},
        }
        self.assertEqual(mcp_transports.transport_for(entry), "container")

    def test_unknown_holder_and_unknown_transport_are_rejected(self) -> None:
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            mcp_transports.transport_for({"name": "x", "placement": {"holder_class": "toaster"}})
        self.assertIn("unknown placement.holder_class", str(ctx.exception))

        entry = {
            "name": "x",
            "placement": {"holder_class": "kali"},
            "runner": {"node": {"transport": "carrier-pigeon"}},
        }
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            mcp_transports.transport_for(entry)
        self.assertIn("unknown node transport", str(ctx.exception))

    def test_registry_policy_can_remap_a_holder(self) -> None:
        policy = mcp_transports.normalise_policy(
            {"policy": {"node_transports": {"holder_defaults": {"kali": "container"}}}}
        )
        entry = {"name": "x", "placement": {"holder_class": "kali"}}
        self.assertEqual(mcp_transports.transport_for(entry, policy=policy), "container")

    def test_real_registry_declares_the_transport_policy(self) -> None:
        policy = mcp_transports.normalise_policy(collab_mcp.load_registry())
        self.assertEqual(policy["holder_defaults"]["flare_vm"], "vmrun_guest")
        self.assertTrue(policy["probe_env"])
        self.assertEqual(
            (REPO_ROOT / policy["guest_bridge"]).resolve(), NODE_BRIDGE.resolve()
        )
        self.assertEqual(
            (REPO_ROOT / policy["vmrun_bridge"]).resolve(), VMRUN_BRIDGE.resolve()
        )


class ProbePythonTests(unittest.TestCase):
    def test_unprovisioned_probe_environment_is_reported_with_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            policy = {"probe_env": ".agent/mcp/.verify/missing-probe"}
            with self.assertRaises(mcp_transports.TransportError) as ctx:
                mcp_transports.resolve_probe_python(
                    {"name": "x"}, repo_root=Path(tmp), policy=policy
                )
            message = str(ctx.exception)
            self.assertIn("not provisioned", message)
            self.assertIn("python -m venv", message)

    def test_entry_level_probe_env_overrides_the_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_probe_env(root, "policy-probe")
            make_probe_env(root, "entry-probe")
            entry = {"name": "x", "runner": {"node": {"probe_env": ".agent/mcp/.verify/entry-probe"}}}
            resolved = mcp_transports.resolve_probe_python(
                entry, repo_root=root, policy={"probe_env": ".agent/mcp/.verify/policy-probe"}
            )
            self.assertIn("entry-probe", str(resolved))


class SshPlanTests(unittest.TestCase):
    def plan(self, entry: dict | None = None):
        return mcp_transports.plan_launch(
            entry or ssh_entry(),
            transport="ssh",
            repo_root=REPO_ROOT,
            probe_python=Path(sys.executable),
            policy={},
            guest_bridge=NODE_BRIDGE,
            vmrun_bridge=VMRUN_BRIDGE,
            which=fake_which({"ssh": "/usr/bin/ssh"}),
        )

    def test_plan_targets_ssh_with_holder_addressing_and_batchmode(self) -> None:
        plan = self.plan()
        self.assertEqual(plan["command"], "/usr/bin/ssh")
        self.assertEqual(plan["secret_names"], ["KALI_HOST", "KALI_USER"])
        self.assertEqual(plan["forwarded_secrets"], [])
        self.assertIn("-o", plan["args"])
        self.assertIn("BatchMode=yes", plan["args"])
        self.assertEqual(plan["args"][-2].count("@"), 1)

    def test_remote_command_survives_a_shell_round_trip(self) -> None:
        plan = self.plan()
        remote = plan["args"][-1]
        self.assertTrue(remote.startswith("sh -c "))
        split = shlex.split(remote)
        self.assertEqual(split[:2], ["sh", "-c"])
        inner = split[2]
        # Values with spaces stay single arguments, and nothing is expanded early.
        self.assertEqual(
            inner,
            "cd /opt/mcp && exec env PATH=/opt/mcp/bin:$PATH MCP_LABEL='a b' "
            "/opt/mcp/bin/server --mode stdio --label 'two words'",
        )
        self.assertEqual(
            shlex.split(inner.replace("cd /opt/mcp && exec env", "").replace("PATH=/opt/mcp/bin:$PATH", "")),
            [
                "MCP_LABEL=a b",
                "/opt/mcp/bin/server",
                "--mode",
                "stdio",
                "--label",
                "two words",
            ],
        )

    @unittest.skipUnless(shutil.which("sh"), "needs a POSIX shell to execute the remote script")
    def test_remote_script_executes_literally_under_a_real_shell(self) -> None:
        entry = ssh_entry()
        entry["runner"]["node"]["exec"] = {
            "command": "printf",
            "args": ["%s|", "two words", "a$b"],
            "env": {"MCP_LABEL": "l a b"},
        }
        plan = self.plan(entry)
        script = shlex.split(plan["args"][-1])[2]
        proc = subprocess.run(
            ["sh", "-c", script], capture_output=True, text=True, timeout=30
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        # ``two words`` stays one argument and ``$b`` is not expanded.
        self.assertEqual(proc.stdout, "two words|a$b|")

    def test_missing_ssh_binary_is_reported(self) -> None:
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            mcp_transports.plan_launch(
                ssh_entry(),
                transport="ssh",
                repo_root=REPO_ROOT,
                probe_python=Path(sys.executable),
                policy={},
                guest_bridge=NODE_BRIDGE,
                vmrun_bridge=VMRUN_BRIDGE,
                which=fake_which({}),
            )
        self.assertIn("'ssh' is required", str(ctx.exception))

    def test_password_auth_requires_sshpass_and_passes_it_through_the_environment(self) -> None:
        entry = ssh_entry(password_secret="KALI_PASSWORD")
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            self.plan(entry)
        self.assertIn("sshpass", str(ctx.exception))

        plan = mcp_transports.plan_launch(
            entry,
            transport="ssh",
            repo_root=REPO_ROOT,
            probe_python=Path(sys.executable),
            policy={},
            guest_bridge=NODE_BRIDGE,
            vmrun_bridge=VMRUN_BRIDGE,
            which=fake_which({"ssh": "/usr/bin/ssh", "sshpass": "/usr/bin/sshpass"}),
        )
        self.assertEqual(plan["command"], "/usr/bin/sshpass")
        self.assertEqual(plan["args"][:2], ["-e", "/usr/bin/ssh"])
        self.assertIn("KALI_PASSWORD", plan["secret_names"])
        # Describe mode renders the value as a placeholder: nothing leaks.
        self.assertEqual(plan["env"], {"SSHPASS": "<KALI_PASSWORD>"})
        self.assertNotIn("KALI_PASSWORD", " ".join(plan["args"]))

        # Execute mode resolves it into the wrapper environment, still not argv.
        resolved = mcp_transports.plan_launch(
            entry,
            transport="ssh",
            repo_root=REPO_ROOT,
            probe_python=Path(sys.executable),
            policy={},
            guest_bridge=NODE_BRIDGE,
            vmrun_bridge=VMRUN_BRIDGE,
            which=fake_which({"ssh": "/usr/bin/ssh", "sshpass": "/usr/bin/sshpass"}),
            secret_lookup=lambda name: {
                "KALI_HOST": "10.0.0.5",
                "KALI_USER": "analyst",
                "KALI_PASSWORD": "hunter2",
            }[name],
        )
        self.assertEqual(resolved["env"], {"SSHPASS": "hunter2"})
        self.assertIn("analyst@10.0.0.5", resolved["args"])
        self.assertNotIn("hunter2", " ".join(resolved["args"]))

    def test_exec_env_may_not_reference_a_secret(self) -> None:
        entry = ssh_entry()
        entry["runner"]["node"]["exec"]["env"] = {"TOKEN": {"secret": "SOME_TOKEN"}}
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            self.plan(entry)
        self.assertIn("must not travel to a node", str(ctx.exception))


class ContainerPlanTests(unittest.TestCase):
    def plan(self, entry: dict | None = None):
        return mcp_transports.plan_launch(
            entry or container_entry(),
            transport="container",
            repo_root=REPO_ROOT,
            probe_python=Path(sys.executable),
            policy={},
            guest_bridge=NODE_BRIDGE,
            vmrun_bridge=VMRUN_BRIDGE,
            which=fake_which({"docker": "/usr/bin/docker"}),
        )

    def test_plan_forwards_stdio_and_defaults_to_no_network(self) -> None:
        plan = self.plan()
        self.assertEqual(plan["command"], "/usr/bin/docker")
        self.assertEqual(plan["args"][:4], ["run", "--rm", "-i", "--network"])
        self.assertEqual(plan["args"][4], "none")
        self.assertIn(str(REPO_ROOT / ".agent" / "mcp" / ".verify") + ":/work:ro", plan["args"])
        self.assertEqual(
            plan["args"][-4:], ["python:3.12-alpine", "python3", "/work/scan.py", "--stdio"]
        )
        self.assertEqual(plan["forwarded_secrets"], [])

    def test_mounts_may_not_escape_the_repository(self) -> None:
        for host in ("/tmp", "C:/Users", "../outside"):
            with self.subTest(host=host):
                with self.assertRaises(mcp_transports.TransportError) as ctx:
                    self.plan(container_entry(mounts=[{"host": host, "container": "/work"}]))
                self.assertIn("outside the repository", str(ctx.exception))

    def test_mount_target_must_be_absolute_and_mode_known(self) -> None:
        with self.assertRaises(mcp_transports.TransportError):
            self.plan(container_entry(mounts=[{"host": ".agent/mcp/.verify", "container": "work"}]))
        with self.assertRaises(mcp_transports.TransportError):
            self.plan(
                container_entry(mounts=[{"host": ".agent/mcp/.verify", "container": "/work", "mode": "z"}])
            )

    def test_declared_secrets_are_forwarded_by_name_never_by_value(self) -> None:
        plan = self.plan(container_entry(secrets=["SEMGREP_APP_TOKEN"]))
        self.assertIn("-e", plan["args"])
        self.assertIn("SEMGREP_APP_TOKEN", plan["args"])
        self.assertEqual(plan["secret_names"], ["SEMGREP_APP_TOKEN"])
        self.assertEqual(plan["forwarded_secrets"], ["SEMGREP_APP_TOKEN"])
        self.assertNotIn("=", plan["args"][plan["args"].index("SEMGREP_APP_TOKEN")])

    def test_secret_names_are_validated(self) -> None:
        with self.assertRaises(mcp_transports.TransportError):
            self.plan(container_entry(secrets=["not a name"]))

    def test_exec_env_is_passed_literally(self) -> None:
        entry = container_entry()
        entry["runner"]["node"]["exec"]["env"] = {"MCP_MODE": "stdio"}
        plan = self.plan(entry)
        self.assertIn("MCP_MODE=stdio", plan["args"])


class VmrunPlanTests(unittest.TestCase):
    def plan(self, entry: dict):
        return mcp_transports.plan_launch(
            entry,
            transport="vmrun_guest",
            repo_root=REPO_ROOT,
            probe_python=Path(sys.executable),
            policy={},
            guest_bridge=NODE_BRIDGE,
            vmrun_bridge=VMRUN_BRIDGE,
        )

    def entry(self, **vmrun_overrides) -> dict:
        vmrun = {"vmx": {"secret": "FLARE_VMX"}}
        vmrun.update(vmrun_overrides)
        return {
            "name": "flare-parser",
            "placement": {"holder_class": "flare_vm"},
            "runner": {
                "node": {
                    "transport": "vmrun_guest",
                    "vmrun": vmrun,
                    "exec": {"command": r"C:\Tools\DFIR\parser.exe", "args": ["--stdio"]},
                }
            },
        }

    def test_plan_runs_the_bridge_on_the_host_and_names_node_secrets(self) -> None:
        plan = self.plan(self.entry())
        self.assertEqual(plan["command"], sys.executable)
        self.assertEqual(plan["args"][0], str(VMRUN_BRIDGE))
        self.assertEqual(
            plan["secret_names"], ["FLARE_VMX", "VM_GU", "VM_GP"]
        )
        self.assertIn("--vmx-env", plan["args"])
        self.assertIn("--guest-user-env", plan["args"])
        self.assertIn("--guest-password-env", plan["args"])
        self.assertEqual(plan["forwarded_secrets"], [])
        self.assertIn(json.dumps([r"C:\Tools\DFIR\parser.exe", "--stdio"]), plan["args"])

    def test_literal_vmx_is_accepted_and_keeps_credentials_from_the_environment(self) -> None:
        plan = self.plan(self.entry(vmx=r"C:\VMs\FLARE-VM\FLARE-VM.vmx"))
        self.assertNotIn("FLARE_VMX", plan["secret_names"])
        self.assertIn(r"C:\VMs\FLARE-VM\FLARE-VM.vmx", plan["args"])

    def test_missing_bridge_scripts_are_reported(self) -> None:
        with self.assertRaises(mcp_transports.TransportError):
            mcp_transports.plan_launch(
                self.entry(),
                transport="vmrun_guest",
                repo_root=REPO_ROOT,
                probe_python=Path(sys.executable),
                policy={},
                guest_bridge=REPO_ROOT / "does-not-exist.py",
                vmrun_bridge=VMRUN_BRIDGE,
            )

    def test_node_transport_without_a_node_block_is_reported(self) -> None:
        with self.assertRaises(mcp_transports.TransportError) as ctx:
            mcp_transports.plan_launch(
                {"name": "x", "placement": {"holder_class": "kali"}},
                transport="ssh",
                repo_root=REPO_ROOT,
                probe_python=Path(sys.executable),
                policy={},
                guest_bridge=NODE_BRIDGE,
                vmrun_bridge=VMRUN_BRIDGE,
                which=fake_which({"ssh": "/usr/bin/ssh"}),
            )
        self.assertIn("needs a runner.node block", str(ctx.exception))

    def test_stdio_local_is_not_a_node_transport(self) -> None:
        with self.assertRaises(mcp_transports.TransportError):
            self.plan({"name": "x", "placement": {"holder_class": "host_gateway"}})


class NodeBridgeUnitTests(unittest.TestCase):
    def test_partial_lines_are_withheld_until_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "responses.jsonl"
            path.write_text("", encoding="utf-8")
            import mcp_node_bridge as node_bridge

            offset = 0
            with path.open("a", encoding="utf-8") as handle:
                handle.write('{"jsonrpc":"2.0"')
            lines, offset = node_bridge._read_new_lines(str(path), offset)
            self.assertEqual(lines, [])
            self.assertEqual(offset, 0)

            with path.open("a", encoding="utf-8") as handle:
                handle.write(',"id":1}\n{"jsonrpc":"2.0","id":2}\n')
            lines, offset = node_bridge._read_new_lines(str(path), offset)
            self.assertEqual(lines, ['{"jsonrpc":"2.0","id":1}', '{"jsonrpc":"2.0","id":2}'])

            lines, offset = node_bridge._read_new_lines(str(path), offset)
            self.assertEqual(lines, [])

    def test_shutdown_sentinel_cannot_be_confused_with_a_message(self) -> None:
        import mcp_node_bridge as node_bridge

        self.assertEqual(node_bridge.SHUTDOWN_SENTINEL, "__MCP_BRIDGE_SHUTDOWN__")
        with self.assertRaises(json.JSONDecodeError):
            json.loads(node_bridge.SHUTDOWN_SENTINEL)

    def test_argv_can_be_json_or_a_shell_line(self) -> None:
        import mcp_node_bridge as node_bridge

        self.assertEqual(node_bridge.parse_argv('["python3","/opt/s.py"]'), ["python3", "/opt/s.py"])
        self.assertEqual(node_bridge.parse_argv("python3 /opt/s.py"), ["python3", "/opt/s.py"])

    def test_node_bridge_runs_from_a_staged_config_and_cleans_up(self) -> None:
        """The guest side must work from one simple argument and clean up after itself."""
        import mcp_node_bridge as node_bridge

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stage = root / "stage"
            stage.mkdir()
            bridge = stage / "mcp_node_bridge.py"
            bridge.write_text(NODE_BRIDGE.read_text(encoding="utf-8"), encoding="utf-8")
            server = root / "echo_mcp.py"
            server.write_text(textwrap.dedent(ECHO_SERVER), encoding="utf-8")
            requests = stage / "requests.jsonl"
            responses = stage / "responses.jsonl"
            ready = stage / "ready.txt"
            config = stage / "bridge-config.json"
            requests.write_text("", encoding="utf-8")
            config.write_text(
                json.dumps(
                    {
                        "argv": [sys.executable, str(server)],
                        "requests": str(requests),
                        "responses": str(responses),
                        "ready_file": str(ready),
                        "idle": 30,
                        "cleanup_grace": 0.2,
                    }
                ),
                encoding="utf-8",
            )
            proc = subprocess.Popen(
                [sys.executable, str(bridge), "--config", str(config)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                deadline = time.time() + 20
                while not ready.exists() and time.time() < deadline:
                    time.sleep(0.1)
                self.assertTrue(ready.exists(), "bridge never reported ready")

                with requests.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n")
                deadline = time.time() + 20
                while time.time() < deadline:
                    if responses.exists() and "echo-node" in responses.read_text(encoding="utf-8"):
                        break
                    time.sleep(0.1)
                self.assertIn("echo-node", responses.read_text(encoding="utf-8"))

                with requests.open("a", encoding="utf-8") as handle:
                    handle.write(node_bridge.SHUTDOWN_SENTINEL + "\n")
                self.assertEqual(proc.wait(timeout=30), 0)
            finally:
                if proc.poll() is None:
                    proc.kill()
                for stream in (proc.stdout, proc.stderr):
                    if stream is not None:
                        stream.close()
            # Everything the host staged is gone, including the bridge itself.
            self.assertEqual(sorted(path.name for path in stage.iterdir()), [])


class VmrunBridgeRoundTripTests(unittest.TestCase):
    """Drive the real host and guest bridges through a faux vmrun."""

    def test_mcp_messages_round_trip_and_guest_scratch_is_cleaned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # The guest bridge runs as a host process in this test, so the guest
            # directory is a real directory and the faux vmrun maps it onto
            # itself: only the guest-operations calls are stubbed, nothing else.
            guest_dir = root / "guest" / "mcp-bridge"
            guest_dir.mkdir(parents=True)
            launcher = fake_vmrun.install(root / "bin", guest_dir, guest_prefix=str(guest_dir))
            echo_server = root / "echo_mcp.py"
            echo_server.write_text(textwrap.dedent(ECHO_SERVER), encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(VMRUN_BRIDGE),
                    "--vmrun-exe",
                    str(launcher),
                    "--vmx",
                    r"C:\VMs\FLARE-VM\FLARE-VM.vmx",
                    "--guest-user",
                    "analyst",
                    "--guest-password",
                    "guest-pass",
                    "--guest-dir",
                    str(guest_dir),
                    "--guest-python",
                    "python.exe",
                    "--guest-bridge",
                    str(NODE_BRIDGE),
                    "--exec-argv",
                    json.dumps([sys.executable, str(echo_server)]),
                    "--poll",
                    "0.1",
                    "--drain",
                    "0.6",
                    "--idle",
                    "30",
                    "--copy-timeout",
                    "20",
                    "--response-timeout",
                    "30",
                ],
                input=(
                    json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
                    + "\n"
                    + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
                    + "\n"
                ),
                capture_output=True,
                text=True,
                timeout=90,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            messages = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
            self.assertEqual([message["id"] for message in messages], [1, 2])
            self.assertEqual(messages[0]["result"]["serverInfo"]["name"], "echo-node")
            self.assertEqual(messages[1]["result"]["tools"][0]["name"], "ping")

            # The shutdown sentinel asked the guest bridge to stop, and the host
            # removed the files it staged into the guest.
            self.assertEqual(sorted(path.name for path in guest_dir.iterdir()), [])

    def test_missing_credentials_fail_fast_instead_of_hanging(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            guest_root = root / "guest"
            guest_root.mkdir()
            launcher = fake_vmrun.install(root / "bin", guest_root)
            env = {k: v for k, v in os.environ.items() if k not in ("VM_GU", "VM_GP")}
            proc = subprocess.run(
                [
                    sys.executable,
                    str(VMRUN_BRIDGE),
                    "--vmrun-exe",
                    str(launcher),
                    "--vmx",
                    r"C:\VMs\FLARE-VM\FLARE-VM.vmx",
                    "--guest-user-env",
                    "VM_GU",
                    "--guest-password-env",
                    "VM_GP",
                    "--guest-dir",
                    r"C:\Windows\Temp\mcp-bridge",
                    "--guest-bridge",
                    str(NODE_BRIDGE),
                    "--exec-argv",
                    json.dumps(["python", "-c", "pass"]),
                ],
                input=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n",
                capture_output=True,
                text=True,
                env=env,
                timeout=60,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("guest credentials missing", proc.stderr)

    def test_vmrun_calls_always_carry_a_timeout(self) -> None:
        """A credential-less vmrun hangs; the client must surface that as an error."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            guest_root = root / "guest"
            guest_root.mkdir()
            launcher = fake_vmrun.install(root / "bin", guest_root)
            os.environ["FAKE_HANG_WITHOUT_CREDS"] = "1"
            os.environ["FAKE_HANG_SECONDS"] = "5"
            try:
                sys.path.insert(0, str(REPO_ROOT / ".agent" / "mcp" / "tools"))
                import mcp_vmrun_bridge as host_bridge

                staged = root / "requests.jsonl"
                staged.write_text("", encoding="utf-8")
                client = host_bridge.VmrunClient(str(launcher), r"C:\vm.vmx", None, None, timeout=1.0)
                with self.assertRaises(host_bridge.BridgeError) as ctx:
                    client.put(staged, r"C:\Windows\Temp\mcp-bridge\requests.jsonl")
                self.assertIn("timed out", str(ctx.exception))
                self.assertIn("credentials", str(ctx.exception))
            finally:
                os.environ.pop("FAKE_HANG_WITHOUT_CREDS", None)
                os.environ.pop("FAKE_HANG_SECONDS", None)


class CollabIntegrationTests(unittest.TestCase):
    def _registry(self, probe_rel: str, entry: dict) -> dict:
        return {
            "version": 1,
            "policy": {"node_transports": {"probe_env": probe_rel}},
            "authorization": {"policy_version": 1, "default_decision": "deny"},
            "servers": [entry],
        }

    def test_resolve_session_plan_switches_transport_with_placement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_probe_env(root, "probe-env")
            policy_rel = str((root / ".agent" / "mcp" / ".verify" / "probe-env").resolve())
            entry = ssh_entry()
            entry["runner"]["venv"] = "unused"
            entry["runner"]["script"] = "unused"
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                plan = collab_mcp.resolve_session_plan(
                    entry, self._registry(policy_rel, entry)
                )
            self.assertEqual(plan["transport"], "ssh")
            self.assertEqual(plan["holder"], "kali")
            self.assertIn("probe-env", plan["probe_python"])

    def test_node_transport_refuses_server_secrets_before_spawning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_probe_env(root, "probe-env")
            policy_rel = str((root / ".agent" / "mcp" / ".verify" / "probe-env").resolve())
            entry = ssh_entry()
            entry["secrets_binding"] = {"required": True, "env": ["SEMGREP_APP_TOKEN"]}
            registry = self._registry(policy_rel, entry)
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                with self.assertRaises(ValueError) as ctx:
                    collab_mcp.run_session(registry, "kali-scanner")
            message = str(ctx.exception)
            self.assertIn("cannot reach a ssh node", message)
            self.assertIn("SEMGREP_APP_TOKEN", message)

    def test_container_transport_may_forward_a_declared_secret(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_probe_env(root, "probe-env")
            policy_rel = str((root / ".agent" / "mcp" / ".verify" / "probe-env").resolve())
            entry = container_entry(secrets=["SEMGREP_APP_TOKEN"])
            entry["secrets_binding"] = {"required": True, "env": ["SEMGREP_APP_TOKEN"]}
            registry = self._registry(policy_rel, entry)
            with patch.object(collab_mcp.protocol, "REPO_ROOT", root):
                with patch.dict(os.environ, {"SEMGREP_APP_TOKEN": "token-value"}):
                    plan = collab_mcp.resolve_session_plan(entry, registry)
                self.assertEqual(plan["transport"], "container")
                self.assertEqual(plan["forwarded_secrets"], ["SEMGREP_APP_TOKEN"])
                # Forwarded by name only; the value rides in the docker client env.
                self.assertIn("SEMGREP_APP_TOKEN", plan["args"])
                self.assertNotIn("token-value", " ".join(plan["args"]))
                self.assertEqual(plan["env"], {"SEMGREP_APP_TOKEN": "token-value"})

                # Missing value: the plan must fail before anything is spawned.
                with patch.dict(os.environ, {}, clear=False):
                    os.environ.pop("SEMGREP_APP_TOKEN", None)
                    with self.assertRaises(mcp_transports.TransportError) as ctx:
                        collab_mcp.resolve_session_plan(entry, registry)
                self.assertIn("missing required secret env name", str(ctx.exception))

    def test_gate_audit_records_the_transport(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "gate.jsonl"
            collab_mcp.record_gate_decision(
                {"server": "x", "tool": "t", "decision": "allow", "reason": "ok"},
                reason="because",
                transport="ssh",
                node="kali",
                log_path=log,
            )
            record = json.loads(log.read_text(encoding="utf-8").strip())
            self.assertEqual(record["transport"], "ssh")
            self.assertEqual(record["node"], "kali")
            self.assertEqual(record["authorized_reason"], "because")


if __name__ == "__main__":
    unittest.main()
