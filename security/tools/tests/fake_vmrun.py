#!/usr/bin/env python3
r"""A stand-in for ``vmrun`` used by the node-transport tests.

VMware is not installed on every machine that runs this suite, and a test that
needs a powered-on guest is a test that never runs. This helper emulates exactly
the Guest Operations the vmrun bridge depends on, with the guest filesystem mapped
onto a temporary directory:

======================  ====================================================
real vmrun command      emulation
======================  ====================================================
``createDirectoryInGuest``  ``mkdir -p`` under the fake guest root
``deleteFileInGuest``       ``unlink`` (missing file -> non-zero exit)
``fileExistsInGuest``       existence check
``CopyFileFromHostToGuest`` real copy (host path -> fake guest path)
``CopyFileFromGuestToHost`` real copy (fake guest path -> host path)
``runProgramInGuest``       ``Popen`` the guest program, ``-noWait`` = detached
======================  ====================================================

``copyFileFromHostToGuest`` overwrites an existing destination, mirroring the
vmrun behaviour the bridge relies on when it re-pushes its request file.

Guest paths are mapped with ``FAKE_GUEST_ROOT`` (host directory) and
``FAKE_GUEST_PREFIX`` (the guest directory that prefix corresponds to); any other
absolute guest path is mirrored under the root, so a test cannot escape it. A
bare program name such as ``python.exe`` is resolved to the running interpreter,
which is what a guest's PATH lookup would do.

``FAKE_HANG_WITHOUT_CREDS=1`` makes a call without ``-gu`` hang instead of
failing, which is how real ``vmrun`` behaves when guest credentials are missing -
that is what the bridge's timeouts exist for.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REQUIRES_AUTH = {
    "createDirectoryInGuest",
    "deleteFileInGuest",
    "fileExistsInGuest",
    "CopyFileFromHostToGuest",
    "CopyFileFromGuestToHost",
    "runProgramInGuest",
    "listProcessesInGuest",
    "listDirectoryInGuest",
}


def guest_to_host(guest_path: str) -> Path:
    """Map a guest path onto the fake guest root."""
    root = Path(os.environ["FAKE_GUEST_ROOT"])
    prefix = os.environ.get("FAKE_GUEST_PREFIX", r"C:\Windows\Temp\mcp-bridge").replace("\\", "/").rstrip("/")
    normalised = guest_path.replace("\\", "/")
    if prefix and normalised.startswith(prefix):
        remainder = normalised[len(prefix) :].strip("/")
        return root / remainder if remainder else root
    parts = [part for part in normalised.split("/") if part and part not in (".", "..")]
    return root.joinpath(*parts)


def _resolve_program(program: str) -> str:
    """Absolute guest paths map into the fake root; bare names behave like PATH lookup."""
    if "/" in program or "\\" in program or ":" in program:
        return str(guest_to_host(program))
    return sys.executable


def main(argv: list[str]) -> int:
    if not argv or argv[0] != "-T":
        print("fake vmrun: expected -T <product>", file=sys.stderr)
        return 1
    args = argv[2:]
    authenticated = False
    while len(args) >= 2 and args[0] in ("-gu", "-gp"):
        authenticated = authenticated or args[0] == "-gu"
        args = args[2:]
    if not args:
        print("fake vmrun: missing command", file=sys.stderr)
        return 1

    command, rest = args[0], args[1:]
    if command in REQUIRES_AUTH and not authenticated:
        if os.environ.get("FAKE_HANG_WITHOUT_CREDS") == "1":
            # Real vmrun blocks forever (no timeout of its own) on a missing
            # -gu/-gp pair. Two details make this usable in a test: the inherited
            # pipes are detached first, so killing the launcher actually unblocks
            # the caller, and the pause stays short (the caller's timeout is much
            # shorter) so the suite does not pay for a long orphan lifetime.
            try:
                devnull = os.open(os.devnull, os.O_RDWR)
                os.dup2(devnull, 1)
                os.dup2(devnull, 2)
            except OSError:
                pass
            time.sleep(float(os.environ.get("FAKE_HANG_SECONDS", "3")))
        print("fake vmrun: authentication failed (no -gu)", file=sys.stderr)
        return 1
    if not rest:
        print(f"fake vmrun: {command} needs a vmx path", file=sys.stderr)
        return 1
    operands = rest[1:]  # rest[0] is the VMX path

    if command == "checkToolsState":
        print("running")
        return 0
    if command == "getGuestIPAddress":
        print("192.168.12.129")
        return 0
    if command == "createDirectoryInGuest":
        guest_to_host(operands[0]).mkdir(parents=True, exist_ok=True)
        return 0
    if command == "deleteFileInGuest":
        target = guest_to_host(operands[0])
        if not target.exists():
            print(f"fake vmrun: no such file {operands[0]}", file=sys.stderr)
            return 1
        target.unlink()
        return 0
    if command == "fileExistsInGuest":
        exists = guest_to_host(operands[0]).exists()
        print("exists" if exists else "not found")
        return 0 if exists else 1
    if command == "CopyFileFromHostToGuest":
        source, target = Path(operands[0]), guest_to_host(operands[1])
        if not source.exists():
            print(f"fake vmrun: host file missing {source}", file=sys.stderr)
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return 0
    if command == "CopyFileFromGuestToHost":
        source, target = guest_to_host(operands[0]), Path(operands[1])
        if not source.exists():
            print(f"fake vmrun: guest file missing {operands[0]}", file=sys.stderr)
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return 0
    if command == "listProcessesInGuest":
        print("Process list: fake vmrun has no process table")
        return 0
    if command == "runProgramInGuest":
        detached = False
        if operands and operands[0] == "-noWait":
            detached = True
            operands = operands[1:]
        if not operands:
            print("fake vmrun: runProgramInGuest needs a program", file=sys.stderr)
            return 1
        program = _resolve_program(operands[0])
        trailing = [str(argument) for argument in operands[1:]]
        try:
            if detached:
                subprocess.Popen(
                    [program, *trailing],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.run([program, *trailing], check=False)
        except OSError as exc:
            print(f"fake vmrun: cannot start {program}: {exc}", file=sys.stderr)
            return 1
        print("Guest program started")
        return 0

    print(f"fake vmrun: unsupported command {command}", file=sys.stderr)
    return 1


def install(directory: Path, guest_root: Path, guest_prefix: str = r"C:\Windows\Temp\mcp-bridge") -> Path:
    """Write a launcher that behaves like ``vmrun`` and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    root = str(guest_root)
    if os.name == "nt":
        launcher = directory / "vmrun.cmd"
        launcher.write_text(
            "@echo off\r\n"
            f'set "FAKE_GUEST_ROOT={root}"\r\n'
            f'set "FAKE_GUEST_PREFIX={guest_prefix}"\r\n'
            f'"{sys.executable}" "{Path(__file__).resolve()}" %*\r\n',
            encoding="utf-8",
        )
    else:
        launcher = directory / "vmrun"
        launcher.write_text(
            "#!/bin/sh\n"
            f"FAKE_GUEST_ROOT='{root}'\n"
            f"FAKE_GUEST_PREFIX='{guest_prefix}'\n"
            "export FAKE_GUEST_ROOT FAKE_GUEST_PREFIX\n"
            f'exec "{sys.executable}" "{Path(__file__).resolve()}" "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)
    return launcher


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
