"""
Unified Challenge Synchronization CLI

Command-line entrypoint for synchronizing and cataloging challenges from various
cybersecurity learning platforms into normalized CSV and Markdown catalogs.

Usage:
  python -m security.challenges.sync.main --platform mta
  python -m security.challenges.sync.main --platform cyberdefenders
  python -m security.challenges.sync.main --all
  python -m security.challenges.sync.main --list
"""

import argparse
import sys
from pathlib import Path
from typing import List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from security.challenges.sync.platforms import ALL_ADAPTERS


def find_repo_root() -> Path:
    """Find repository root dynamically."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists() or (parent / "security").exists():
            return parent
    return current.parent.parent.parent.parent


def main():
    parser = argparse.ArgumentParser(
        description="Unified Challenge Sync Framework CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--platform",
        "-p",
        choices=list(ALL_ADAPTERS.keys()),
        help="Target platform to synchronize.",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Synchronize all available platforms.",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all registered platform adapters.",
    )

    args = parser.parse_args()

    if args.list:
        print("\nRegistered Platform Adapters:")
        for key, cls in ALL_ADAPTERS.items():
            print(f"  - {key:<16} : {cls.display_name}")
        print()
        sys.exit(0)

    if not args.platform and not args.all:
        parser.print_help()
        sys.exit(1)

    repo_root = find_repo_root()
    selected_keys: List[str] = []
    if args.all:
        selected_keys = list(ALL_ADAPTERS.keys())
    elif args.platform:
        selected_keys = [args.platform]

    results = []
    for key in selected_keys:
        adapter_cls = ALL_ADAPTERS[key]
        adapter = adapter_cls(repo_root=repo_root)
        try:
            res = adapter.sync()
            results.append(res)
        except Exception as e:
            print(f"[!] Error syncing {key}: {e}")
            results.append({"platform_id": key, "display_name": key, "error": str(e)})

    # Summary Report
    print("\n========================================================")
    print("CHALLENGE SYNCHRONIZATION SUMMARY REPORT")
    print("========================================================")
    print(f"{'Platform':22} | {'Total':8} | {'Free Tier':10} | Status")
    print("-" * 56)
    for r in results:
        if "error" in r:
            name = str(r['display_name'])[:22]
            print(f"{name:22} | {'-':8} | {'-':10} | [FAILED] {r['error']}")
        else:
            name = str(r['display_name'])[:22]
            total_str = str(r['total'])
            free_str = str(r['free_count'])
            print(f"{name:22} | {total_str:8} | {free_str:10} | [OK]")
    print("========================================================\n")


if __name__ == "__main__":
    main()
