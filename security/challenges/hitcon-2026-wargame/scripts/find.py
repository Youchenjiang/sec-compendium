#!/usr/bin/env python3
"""
Consolidated entry point finder.
Replaces: find_clean_web_entries, find_core_endpoints, find_true_entrypoints, find_procedural

Usage:
    python scripts/find.py --type web           # Find standalone web entry files
    python scripts/find.py --type core          # Find core endpoints with HTTP input + sinks
    python scripts/find.py --type entrypoint    # Find true procedural entry points
    python scripts/find.py --type procedural    # Find procedural code with superglobals + sinks
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.paths import SCAN_CACHE
from lib.scanner_utils import iter_php_files, read_php_file, has_superglobal, ENTRY_FILENAMES

DANGEROUS_SINKS = ["file_put_contents", "eval", "system", "exec", "shell_exec",
                   "passthru", "include", "require", "unserialize", "assert"]


def find_web_entries():
    """Find standalone index/install/setup files with HTTP input."""
    standalone_entries = []
    for p_dir in SCAN_CACHE.iterdir():
        if not p_dir.is_dir():
            continue
        vendor_root = p_dir / "vendor"
        if not vendor_root.exists():
            continue
        for php_f in vendor_root.rglob("*.php"):
            parts = [p.lower() for p in php_f.parts]
            if any(ex in parts for ex in ["tests", "test", "examples", "docs", "spec"]):
                continue
            if php_f.name not in ["index.php", "install.php", "setup.php", "app.php", "bootstrap.php"]:
                continue
            try:
                content = php_f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            rel = php_f.relative_to(p_dir)
            standalone_entries.append({
                "pkg_dir": p_dir.name,
                "file": str(rel),
                "has_get": "$_GET" in content,
                "has_post": "$_POST" in content,
                "has_request": "$_REQUEST" in content,
                "has_raw": "php://input" in content,
            })

    print(f"Found {len(standalone_entries)} standalone entry files:")
    for se in standalone_entries:
        inputs = []
        if se["has_get"]:
            inputs.append("GET")
        if se["has_post"]:
            inputs.append("POST")
        if se["has_request"]:
            inputs.append("REQUEST")
        if se["has_raw"]:
            inputs.append("RAW")
        print(f"  {se['pkg_dir']:40} -> {se['file']} [{','.join(inputs) or 'NONE'}]")


def find_core_endpoints():
    """Find files with HTTP input AND dangerous sinks in non-dev dirs."""
    results = []
    excluded = {"tests", "test", "examples", "docs", "spec", "features", ".git"}

    for p_dir in SCAN_CACHE.iterdir():
        if not p_dir.is_dir():
            continue
        for php_file in p_dir.rglob("*.php"):
            parts = [p.lower() for p in php_file.parts]
            if any(ex in parts for ex in excluded):
                continue
            try:
                content = php_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            has_http = any(g in content for g in ["$_GET", "$_POST", "$_REQUEST", "php://input"])
            has_sinks = any(s in content for s in ["eval(", "system(", "exec(", "file_put_contents(", "unserialize("])

            if has_http and has_sinks:
                rel_path = php_file.relative_to(p_dir)
                results.append({
                    "pkg_dir": p_dir.name,
                    "file": str(rel_path),
                    "has_eval": "eval(" in content,
                    "has_system": any(s in content for s in ["system(", "exec(", "passthru("]),
                    "has_unserialize": "unserialize(" in content,
                    "has_file_write": "file_put_contents(" in content,
                })

    print(f"\n=== {len(results)} CORE ENTRYPOINTS (HTTP input + dangerous sink) ===")
    for r in sorted(results, key=lambda x: (x["has_system"], x["has_eval"], x["has_unserialize"]), reverse=True)[:30]:
        sinks = []
        if r["has_system"]:
            sinks.append("CMD")
        if r["has_eval"]:
            sinks.append("EVAL")
        if r["has_unserialize"]:
            sinks.append("DESER")
        if r["has_file_write"]:
            sinks.append("WRITE")
        print(f"  [{','.join(sinks):20}] {r['pkg_dir']} -> {r['file']}")


def find_entrypoints():
    """Find true procedural entry points with HTTP input and critical sinks."""
    all_entrypoints = []

    for pkg_dir in SCAN_CACHE.iterdir():
        if not pkg_dir.is_dir():
            continue
        for php_file in iter_php_files(pkg_dir, skip_vendor=True):
            content = read_php_file(php_file)
            if content is None:
                continue

            has_http = has_superglobal(content) or "php://input" in content
            is_entry = php_file.name.lower() in ENTRY_FILENAMES
            if not (has_http or is_entry):
                continue
            if php_file.name.endswith("Test.php"):
                continue

            sinks = []
            if "eval(" in content:
                sinks.append("eval")
            if any(s in content for s in ["system(", "exec(", "passthru(", "shell_exec("]):
                sinks.append("exec")
            if "unserialize(" in content:
                sinks.append("unserialize")
            if "file_put_contents(" in content:
                sinks.append("file_put_contents")
            if "file_get_contents(" in content:
                sinks.append("file_get_contents")

            all_entrypoints.append({
                "pkg": pkg_dir.name,
                "file": str(php_file.relative_to(pkg_dir)),
                "has_http": has_http,
                "sinks": sinks,
            })

    high_priority = [ep for ep in all_entrypoints if ep["has_http"] and any(
        s in ep["sinks"] for s in ["eval", "exec", "unserialize", "file_put_contents"])]

    print(f"Total entry points: {len(all_entrypoints)}")
    print(f"High priority (HTTP + critical sink): {len(high_priority)}")
    for ep in high_priority:
        print(f"  [HIGH] {ep['pkg']:35} -> {ep['file']} ({','.join(ep['sinks'])})")


def find_procedural():
    """Find procedural code with superglobals AND dangerous sinks."""
    results = []
    for pkg_dir in SCAN_CACHE.iterdir():
        if not pkg_dir.is_dir():
            continue
        vendor_dir = pkg_dir / "vendor"
        if not vendor_dir.exists():
            continue
        for php_file in vendor_dir.rglob("*.php"):
            parts = [p.lower() for p in php_file.parts]
            if "composer" in parts or php_file.name == "autoload.php":
                continue
            try:
                content = php_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            has_sg = any(sg in content for sg in ["$_GET", "$_POST", "$_REQUEST", "$_COOKIE"])
            sinks_found = [s for s in DANGEROUS_SINKS if s in content]

            if has_sg and sinks_found:
                rel_path = php_file.relative_to(pkg_dir)
                results.append({
                    "package": pkg_dir.name,
                    "file": str(rel_path),
                    "sinks": sinks_found,
                })

    print(f"=== {len(results)} PROCEDURAL ENTRY POINTS WITH SINKS ===")
    for r in results:
        print(f"[{r['package']}] {r['file']}")
        print(f"   Sinks: {', '.join(r['sinks'])}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Consolidated entry point finder")
    parser.add_argument("--type", required=True, choices=["web", "core", "entrypoint", "procedural"])
    args = parser.parse_args()

    if not SCAN_CACHE.exists():
        print("[-] scan_cache directory does not exist.")
        return 1

    if args.type == "web":
        find_web_entries()
    elif args.type == "core":
        find_core_endpoints()
    elif args.type == "entrypoint":
        find_entrypoints()
    elif args.type == "procedural":
        find_procedural()
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
