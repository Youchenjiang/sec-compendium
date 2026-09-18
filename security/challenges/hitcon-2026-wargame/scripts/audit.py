#!/usr/bin/env python3
"""
Unified Audit — scan specific packages for POP gadgets, sensitive files, and user-input sinks.

Usage:
  python audit.py                        # default: audit next batch
  python audit.py --packages pkg1 pkg2   # audit specific packages
  python audit.py --mode depth           # deep audit for POP gadgets + sensitive files
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.paths import SCAN_CACHE

# Default package lists
DEPTH_PACKAGES = [
    "dompdf_dompdf_3.1.6",
    "drewm_mailchimp-api_2.5.4",
    "erusev_parsedown_1.8.0",
    "filp_whoops_2.18.4",
    "firebase_php-jwt_7.1.0",
    "fzaninotto_faker_1.5.0",
    "gabordemooij_redbean_5.7",
    "guzzlehttp_guzzle_8.0.1",
    "ifsnop_mysqldump-php_2.12",
    "intervention_image_4.2.0",
]

BATCH_PACKAGES = [
    "potsky_pimp-my-log_1.7.10",
    "art-of-wifi_unifi-api-client_2.2.1",
    "vrana_adminer_5.5.1",
    "shardj_zf1-future_1.25.0",
    "propel_propel1_1.7.2",
    "jmose_command-scheduler-bundle_1.2.7",
]

SINKS = ["file_get_contents", "readfile", "highlight_file", "eval", "system", "exec",
         "shell_exec", "passthru", "file_put_contents", "unserialize", "include", "require"]

POP_SINKS = [
    "eval(", "system(", "exec(", "shell_exec(",
    "passthru(", "file_put_contents(", "unlink(", "include", "require"
]


def _check_php_pop_gadgets(php_f, p_dir):
    if "tests" in [part.lower() for part in php_f.parts]:
        return
    try:
        content = php_f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    magic_methods = ("function __destruct", "function __toString", "function __wakeup")
    if any(m in content for m in magic_methods):
        for line_no, line in enumerate(content.split("\n"), 1):
            s = line.strip()
            if any(sink in line for sink in POP_SINKS) and not s.startswith(("//", "*", "#")):
                print(f"  [POP GADGET] {php_f.relative_to(p_dir)}:{line_no} -> {s[:100]}")


def _audit_single_depth(p_name):
    p_dir = SCAN_CACHE / p_name
    if not p_dir.exists():
        return
    print(f"\n[*] Auditing: {p_name}")

    # Sensitive files
    for ext in ["*.pem", "*.key", "*.sql", "*.sqlite", "*.db", "*.env*"]:
        for f in p_dir.rglob(ext):
            print(f"  [SENSITIVE] {f.relative_to(p_dir)}")

    # POP gadget sinks
    for php_f in p_dir.rglob("*.php"):
        _check_php_pop_gadgets(php_f, p_dir)


def audit_depth(pkg_names):
    """Deep audit: POP gadgets + sensitive files."""
    if not SCAN_CACHE.exists():
        print("[-] scan_cache directory does not exist.")
        return
    print("=== DEEP AUDIT: POP GADGETS & GLOBAL HELPERS ===")
    for p in pkg_names:
        _audit_single_depth(p)


def _audit_php_file_sinks(php_file, rel_path):
    try:
        txt = php_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    for idx, line in enumerate(txt.split("\n"), 1):
        s = line.strip()
        if not s or s.startswith(("//", "*", "#")):
            continue
        if any(sink in s for sink in SINKS) and any(src in s for src in ["$_GET", "$_POST", "$_REQUEST"]):
            print(f"[{rel_path}:{idx}] {s[:120]}")


def _audit_single_batch(t_name):
    t_dir = SCAN_CACHE / t_name
    if not t_dir.exists():
        return
    print(f"\n{'=' * 20} {t_name} {'=' * 20}")
    keywords = ["test", "demo", "example", "admin", "install", "tool", "inc", "view", "get", "api"]
    for p in t_dir.rglob("*.php"):
        rel = str(p.relative_to(t_dir)).lower()
        if any(k in rel for k in keywords):
            if "phpunit" in rel or "fixtures" in rel:
                continue
            _audit_php_file_sinks(p, rel)


def audit_batch(pkg_names):
    """Batch audit: find user-input -> sink in specific packages."""
    if not SCAN_CACHE.exists():
        print("[-] scan_cache directory does not exist.")
        return
    print("[*] Auditing next batch of high-priority packages...")
    for t in pkg_names:
        _audit_single_batch(t)


def main():
    parser = argparse.ArgumentParser(description="Unified audit tool")
    parser.add_argument("--mode", choices=["depth", "batch"], default="batch")
    parser.add_argument("--packages", nargs="*", help="Custom package list")
    args = parser.parse_args()

    pkg_list = args.packages or (DEPTH_PACKAGES if args.mode == "depth" else BATCH_PACKAGES)

    if args.mode == "depth":
        audit_depth(pkg_list)
    else:
        audit_batch(pkg_list)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
