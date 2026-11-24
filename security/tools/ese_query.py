#!/usr/bin/env python3
"""Bounded, read-only ESE database inspection for DFIR Race mode."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path


def _open(path: str):
    try:
        from dissect.esedb import EseDB
    except Exception as exc:
        raise RuntimeError(f"dissect.esedb unavailable: {type(exc).__name__}: {exc}") from exc
    database = Path(path).expanduser().resolve()
    if not database.is_file():
        raise ValueError(f"database does not exist: {database}")
    return EseDB(database.open("rb"))


def _jsonable(value):
    if isinstance(value, bytes):
        return {
            "type": "bytes",
            "length": len(value),
            "base64": base64.b64encode(value).decode("ascii"),
        }
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _emit(value) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_tables(args) -> int:
    db = _open(args.database)
    _emit([table.name for table in db.tables()])
    return 0


def command_schema(args) -> int:
    db = _open(args.database)
    table = db.table(args.table)
    _emit({"table": args.table, "columns": list(table.column_names)})
    return 0


def _record_text(raw) -> str:
    """Join a record's values into one casefolded search string."""
    return " ".join(
        (
            value.decode("utf-16le", "ignore")
            if isinstance(value, bytes)
            else str(value)
        )
        for value in raw.values()
    ).casefold()


def command_records(args) -> int:
    db = _open(args.database)
    table = db.table(args.table)
    needle = (args.contains or "").casefold()
    rows = []
    scanned = 0
    for record in table.records():
        scanned += 1
        raw = record.as_dict()
        if needle and needle not in _record_text(raw):
            if scanned >= args.max_scan:
                break
            continue
        rows.append({str(k): _jsonable(v) for k, v in raw.items()})
        if len(rows) >= args.max_rows or scanned >= args.max_scan:
            break
    _emit({"table": args.table, "scanned": scanned, "rows": rows})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only bounded ESE queries")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("tables")
    p.add_argument("--database", required=True)
    p.set_defaults(func=command_tables)
    p = sub.add_parser("schema")
    p.add_argument("--database", required=True)
    p.add_argument("--table", required=True)
    p.set_defaults(func=command_schema)
    p = sub.add_parser("records")
    p.add_argument("--database", required=True)
    p.add_argument("--table", required=True)
    p.add_argument("--contains", default="")
    p.add_argument("--max-rows", type=int, default=20)
    p.add_argument("--max-scan", type=int, default=100000)
    p.set_defaults(func=command_records)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
