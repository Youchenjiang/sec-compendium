#!/usr/bin/env python3
"""
List packages — solved, candidates, or filtered by keywords.

Usage:
  python list.py solved              # list all solved packages
  python list.py candidates          # filter packages by security keywords
  python list.py candidates --kw upload,admin,auth
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.paths import RESULTS_DIR

DEFAULT_KEYWORDS = [
    "rbac", "auth", "admin", "cms", "upload", "file", "template", "sql", "db",
    "install", "setup", "eval", "exec", "system", "cmd", "shell", "backup",
    "manager", "editor", "api", "gateway", "login", "user", "permission", "role",
]


def list_solved():
    data_file = RESULTS_DIR / "all_solved.json"
    if not data_file.exists():
        print(f"[-] {data_file} not found")
        sys.exit(1)

    with open(data_file, "rb") as f:
        data = json.loads(f.read().replace(b"\r\n", b"\n"))

    for p in sorted(data, key=lambda x: x.get("solves", 0), reverse=True)[:40]:
        print(f'{p.get("solves", 0):4d}  {p["name"]}  {p.get("version", "?")}')


def list_candidates(keywords):
    pkgs_file = RESULTS_DIR / "all_packages.json"
    if not pkgs_file.exists():
        print(f"[-] {pkgs_file} not found")
        sys.exit(1)

    with open(pkgs_file, "r", encoding="utf-8") as f:
        all_pkgs = json.load(f)
    selected = []
    seen = set()

    for p in all_pkgs:
        name = p.get("name", "").lower()
        key = (name, p.get("version", ""))
        if key in seen:
            continue
        if any(kw in name for kw in keywords):
            selected.append(p)
            seen.add(key)

    print(f"Found {len(selected)} candidate packages matching keywords")
    for p in selected[:50]:
        print(f'  {p.get("name", ""):40} {p.get("version", ""):10} stars={p.get("stars", 0)}')


def main():
    parser = argparse.ArgumentParser(description="List wargame packages")
    parser.add_argument("mode", choices=["solved", "candidates"])
    parser.add_argument("--kw", help="Comma-separated keywords for candidates mode")
    args = parser.parse_args()

    if args.mode == "solved":
        list_solved()
    else:
        keywords = args.kw.split(",") if args.kw else DEFAULT_KEYWORDS
        list_candidates(keywords)


if __name__ == "__main__":
    main()
