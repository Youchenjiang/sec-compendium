#!/usr/bin/env python3
"""
Unified package downloader for HITCON 2026 Wargame.

Combines functionality from:
- batch_download_548.py (sequential download from candidates list)
- batch_download_robust.py (sequential with timeout handling)
- batch_download_solved.py (parallel download from solved-not-downloaded list)
- retry_failed_downloads.py (retry previously failed downloads)

Usage:
    python download.py                          # default: parallel download solved packages
    python download.py --list candidates        # download from candidates_548.json
    python download.py --list solved            # download from solved_not_downloaded.json
    python download.py --list <path.json>       # download from any JSON list
    python download.py --sequential             # single-threaded
    python download.py --workers 4              # custom worker count
    python download.py --timeout 120            # custom timeout per package
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.paths import SCAN_CACHE, RESULTS_DIR


def download_package(pkg: dict, timeout: int = 90) -> tuple:
    """Download a single package via composer. Returns (pkg, success, message)."""
    name = pkg.get("name", "")
    ver = pkg.get("version", "")
    safe_name = name.replace("/", "_")
    pkg_dir = SCAN_CACHE / f"{safe_name}_{ver}"

    if (pkg_dir / "vendor").exists():
        return (pkg, True, "already exists")

    pkg_dir.mkdir(parents=True, exist_ok=True)

    composer_json = {
        "name": "audit/target",
        "require": {name: ver},
        "config": {"platform-check": False},
    }
    (pkg_dir / "composer.json").write_text(json.dumps(composer_json), encoding="utf-8")

    cmd = "composer update --ignore-platform-reqs --no-plugins --no-dev --no-interaction --prefer-dist --quiet"
    try:
        res = subprocess.run(cmd, cwd=str(pkg_dir), shell=True,
                             capture_output=True, text=True, timeout=timeout)
        if (pkg_dir / "vendor").exists():
            return (pkg, True, "downloaded")
        stderr_short = (res.stderr or "").strip()[:200]
        return (pkg, False, f"no vendor dir: {stderr_short}")
    except subprocess.TimeoutExpired:
        return (pkg, False, f"timeout ({timeout}s)")
    except Exception as e:
        return (pkg, False, str(e)[:200])


def load_candidates(list_arg: str) -> list:
    """Load package list from JSON file or predefined name."""
    list_map = {
        "candidates": RESULTS_DIR / "candidates_548.json",
        "solved": RESULTS_DIR / "solved_not_downloaded.json",
    }
    path = list_map.get(list_arg, Path(list_arg))
    if not path.exists():
        print(f"[-] {path} not found")
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Download wargame packages")
    parser.add_argument("--list", default="solved",
                        help="Package list: 'candidates', 'solved', or path to JSON")
    parser.add_argument("--sequential", action="store_true",
                        help="Single-threaded download")
    parser.add_argument("--workers", type=int, default=8,
                        help="Parallel workers (default: 8)")
    parser.add_argument("--timeout", type=int, default=90,
                        help="Timeout per package in seconds (default: 90)")
    args = parser.parse_args()

    candidates = load_candidates(args.list)
    SCAN_CACHE.mkdir(exist_ok=True)

    print(f"[*] {len(candidates)} packages to download"
          f" ({'sequential' if args.sequential else f'{args.workers} workers'})")
    print(f"[*] Starting at {time.strftime('%H:%M:%S')}\n")

    success = failed = skipped = 0

    if args.sequential:
        for i, pkg in enumerate(candidates, 1):
            _, ok, msg = download_package(pkg, args.timeout)
            if ok:
                skipped += 1 if msg == "already exists" else 0
                success += 1 if msg == "downloaded" else 0
            else:
                failed += 1
            tag = "✅" if ok else "❌"
            print(f"[{i}/{len(candidates)}] {tag} {pkg['name']}:{pkg['version']} — {msg}")
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(download_package, pkg, args.timeout): pkg
                       for pkg in candidates}
            for i, future in enumerate(as_completed(futures), 1):
                pkg, ok, msg = future.result()
                if ok:
                    skipped += 1 if msg == "already exists" else 0
                    success += 1 if msg == "downloaded" else 0
                else:
                    failed += 1
                tag = "✅" if ok else "❌"
                print(f"[{i}/{len(candidates)}] {tag} {pkg['name']}:{pkg['version']} — {msg}")
                if i % 20 == 0:
                    print(f"\n--- Progress: {success} downloaded, {skipped} skipped, {failed} failed ---\n")

    print(f"\n{'=' * 60}")
    print(f"DONE at {time.strftime('%H:%M:%S')}")
    print(f"  Downloaded:  {success}")
    print(f"  Skipped:     {skipped} (already had vendor/)")
    print(f"  Failed:      {failed}")
    print(f"  Total:       {len(candidates)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
