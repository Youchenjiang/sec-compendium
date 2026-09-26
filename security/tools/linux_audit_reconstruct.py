#!/usr/bin/env python3
"""Reconstruct Linux auditd events without requiring ausearch/aureport.

The parser groups raw audit records by ``msg=audit(epoch:serial)`` and joins
SYSCALL / EXECVE / CWD / PATH / PROCTITLE records into one event row.  It is
intended as an offline DFIR fallback when the audit userspace package is not
installed on the analysis host.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import ipaddress
import json
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


AUDIT_ID_RE = re.compile(r"msg=audit\((?P<epoch>\d+(?:\.\d+)?):(?P<serial>\d+)\)")
TYPE_RE = re.compile(r"\btype=(?P<type>[^ ]+)")
FIELD_RE = re.compile(r"(?P<key>[A-Za-z0-9_]+)=(?P<value>\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*'|\S+)")
HEX_RE = re.compile(r"^[0-9A-Fa-f]+$")


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_fields(text: str) -> dict[str, str]:
    # Keep quoting intact. Auditd uses *unquoted* hexadecimal text for encoded
    # string fields; quoted hex-looking text is literal and must not be decoded.
    return {m.group("key"): m.group("value") for m in FIELD_RE.finditer(text)}


def decode_audit_text(value: str) -> str:
    """Decode auditd string syntax while preserving quoted hex literals."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return strip_quotes(value)
    if len(value) < 2 or len(value) % 2 or not HEX_RE.fullmatch(value):
        return value
    try:
        raw = bytes.fromhex(value)
    except ValueError:
        return value
    # audit strings are normally UTF-8 / ASCII.  Reject control-heavy output so
    # pointer-like hex values are not accidentally presented as text.
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return value
    if not decoded:
        return value
    printable = sum(ch.isprintable() or ch in "\t\r\n\x00" for ch in decoded)
    if printable / len(decoded) < 0.9:
        return value
    return decoded


def decode_proctitle(value: str) -> list[str]:
    decoded = decode_audit_text(value)
    return [part for part in decoded.split("\x00") if part]


def plain(fields: dict[str, str], key: str) -> str:
    value = fields.get(key, "")
    return strip_quotes(value) if value else ""


def decode_sockaddr(value: str) -> str:
    """Decode common auditd sockaddr hex for IPv4, IPv6 and Unix sockets."""
    raw_text = strip_quotes(value)
    if len(raw_text) % 2 or not HEX_RE.fullmatch(raw_text):
        return raw_text
    try:
        raw = bytes.fromhex(raw_text)
    except ValueError:
        return raw_text
    if len(raw) < 2:
        return raw_text
    family = int.from_bytes(raw[:2], "little")
    if family == 2 and len(raw) >= 8:  # AF_INET
        port = int.from_bytes(raw[2:4], "big")
        return f"{ipaddress.IPv4Address(raw[4:8])}:{port}"
    if family == 10 and len(raw) >= 24:  # AF_INET6
        port = int.from_bytes(raw[2:4], "big")
        return f"[{ipaddress.IPv6Address(raw[8:24])}]:{port}"
    if family == 1 and len(raw) > 2:  # AF_UNIX
        path = raw[2:].split(b"\x00", 1)[0].decode("utf-8", errors="replace")
        return f"unix:{path}"
    return raw_text


def shell_join(argv: Iterable[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in argv)


@dataclass
class AuditEvent:
    epoch: str
    serial: int
    records: dict[str, list[dict[str, str]]] = field(default_factory=dict)

    def add(self, record_type: str, fields: dict[str, str]) -> None:
        self.records.setdefault(record_type, []).append(fields)

    @property
    def syscall(self) -> dict[str, str]:
        return self.records.get("SYSCALL", [{}])[0]

    @property
    def execve(self) -> dict[str, str]:
        return self.records.get("EXECVE", [{}])[0]

    @property
    def cwd_record(self) -> dict[str, str]:
        return self.records.get("CWD", [{}])[0]

    @property
    def user_cmd_record(self) -> dict[str, str]:
        return self.records.get("USER_CMD", [{}])[0]

    def argv(self) -> list[str]:
        rec = self.execve
        if rec:
            pairs: list[tuple[int, str]] = []
            for key, value in rec.items():
                match = re.fullmatch(r"a(\d+)", key)
                if match:
                    pairs.append((int(match.group(1)), decode_audit_text(value)))
            if pairs:
                return [value for _, value in sorted(pairs)]

        for rec in self.records.get("PROCTITLE", []):
            value = rec.get("proctitle")
            if value:
                decoded = decode_proctitle(value)
                if decoded:
                    return decoded
        return []

    def row(self) -> dict[str, object]:
        syscall = self.syscall
        user_cmd = self.user_cmd_record
        argv = self.argv()
        user_command = ""
        if user_cmd.get("cmd"):
            user_command = decode_audit_text(user_cmd["cmd"])
        paths = [decode_audit_text(p["name"]) for p in self.records.get("PATH", []) if p.get("name")]
        sockaddrs = [decode_sockaddr(s["saddr"]) for s in self.records.get("SOCKADDR", []) if s.get("saddr")]
        timestamp = dt.datetime.fromtimestamp(float(self.epoch), tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")
        return {
            "timestamp_utc": timestamp,
            "epoch": self.epoch,
            "serial": self.serial,
            "event_id": f"{self.epoch}:{self.serial}",
            "pid": plain(syscall, "pid") or plain(user_cmd, "pid"),
            "ppid": plain(syscall, "ppid"),
            "uid": plain(syscall, "uid") or plain(user_cmd, "uid"),
            "gid": plain(syscall, "gid"),
            "euid": plain(syscall, "euid"),
            "egid": plain(syscall, "egid"),
            "auid": plain(syscall, "auid") or plain(user_cmd, "auid"),
            "ses": plain(syscall, "ses") or plain(user_cmd, "ses"),
            "tty": plain(syscall, "tty") or plain(user_cmd, "terminal"),
            "success": plain(syscall, "success") or plain(user_cmd, "res"),
            "arch": plain(syscall, "arch"),
            "syscall": plain(syscall, "syscall"),
            "audit_key": plain(syscall, "key"),
            "comm": decode_audit_text(syscall["comm"]) if syscall.get("comm") else "",
            "exe": decode_audit_text(syscall["exe"]) if syscall.get("exe") else (decode_audit_text(user_cmd["exe"]) if user_cmd.get("exe") else ""),
            "cwd": decode_audit_text(self.cwd_record["cwd"]) if self.cwd_record.get("cwd") else (decode_audit_text(user_cmd["cwd"]) if user_cmd.get("cwd") else ""),
            "argc": plain(self.execve, "argc"),
            "argv": argv,
            "user_command": user_command,
            "command": shell_join(argv) if argv else user_command,
            "paths": paths,
            "sockaddr": sockaddrs,
            "record_types": sorted(self.records),
        }


def parse_audit_log(path: Path) -> list[AuditEvent]:
    events: dict[tuple[str, int], AuditEvent] = {}
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            audit_id = AUDIT_ID_RE.search(line)
            type_match = TYPE_RE.search(line)
            if not audit_id or not type_match:
                continue
            epoch_text = audit_id.group("epoch")
            serial = int(audit_id.group("serial"))
            key = (epoch_text, serial)
            event = events.setdefault(key, AuditEvent(epoch_text, serial))
            payload = line[audit_id.end() :]
            record_type = type_match.group("type")
            fields = parse_fields(payload)
            # USER_CMD stores cwd/cmd/exe/terminal/res inside a quoted nested
            # msg='...' field while pid/uid/auid/ses live on the outer record.
            if record_type == "USER_CMD" and fields.get("msg"):
                fields.update(parse_fields(strip_quotes(fields["msg"])))
            event.add(record_type, fields)
    return sorted(events.values(), key=lambda event: (float(event.epoch), event.serial))


CSV_FIELDS = [
    "timestamp_utc",
    "epoch",
    "serial",
    "event_id",
    "pid",
    "ppid",
    "uid",
    "gid",
    "euid",
    "egid",
    "auid",
    "ses",
    "tty",
    "success",
    "arch",
    "syscall",
    "audit_key",
    "comm",
    "exe",
    "cwd",
    "argc",
    "argv",
    "user_command",
    "command",
    "paths",
    "sockaddr",
    "record_types",
]


def normalized_row(row: dict[str, object]) -> dict[str, object]:
    result = dict(row)
    result["argv"] = json.dumps(row["argv"], ensure_ascii=False)
    result["paths"] = " | ".join(str(x) for x in row["paths"])
    result["sockaddr"] = " | ".join(str(x) for x in row["sockaddr"])
    result["record_types"] = " | ".join(str(x) for x in row["record_types"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_log", type=Path, help="Raw /var/log/audit/audit.log file")
    parser.add_argument(
        "--audit-id",
        help="Show only one full audit event id as <epoch>:<serial> (preferred)",
    )
    parser.add_argument(
        "--serial",
        type=int,
        help="Show all events with this serial; serials can repeat across epochs/boots",
    )
    parser.add_argument("--comm", help="Case-insensitive exact command-name filter")
    parser.add_argument("--csv", type=Path, help="Write reconstructed EXECVE/SYSCALL events to CSV")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable rows")
    args = parser.parse_args()

    if not args.audit_log.is_file():
        parser.error(f"audit log not found: {args.audit_log}")

    events = parse_audit_log(args.audit_log)
    rows = [event.row() for event in events]
    # Command reconstruction is meaningful primarily for execve-style events.
    rows = [row for row in rows if row["command"] or row["comm"] or row["exe"]]

    if args.audit_id:
        rows = [row for row in rows if row["event_id"] == args.audit_id]
    if args.serial is not None:
        rows = [row for row in rows if row["serial"] == args.serial]
    if args.comm:
        wanted = args.comm.casefold()
        rows = [row for row in rows if str(row["comm"]).casefold() == wanted]

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow(normalized_row(row))

    if args.json:
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for row in rows:
            print(
                f"{row['timestamp_utc']} audit_id={row['event_id']} "
                f"pid={row['pid']} ppid={row['ppid']} comm={row['comm']!r} "
                f"cwd={row['cwd']!r} command={row['command']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
