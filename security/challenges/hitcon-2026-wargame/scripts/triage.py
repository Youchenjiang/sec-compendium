#!/usr/bin/env python3
"""
Unified Triage — scan scan_cache for actionable vulnerabilities.

Modes:
  --mode triage        Full autonomous deep-triage (writes dossiers + queue tasks)
  --mode categorize    Categorize vulnerabilities by type (writes actionable vectors JSON)

Usage:
  python triage.py --mode triage
  python triage.py --mode categorize
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.paths import SCAN_CACHE, DATA_DIR

# ── Shared regex patterns ──
SRC_RE = re.compile(
    r"\$_(?:GET|POST|REQUEST|COOKIE|SERVER)\s*\[\s*['\"]([^'\"]+)['\"]\s*\]|php://input|\$argv"
)
SINK_READ_RE = re.compile(
    r"\b(?:file_get_contents|readfile|highlight_file|show_source|include|require|include_once|require_once)\s*\(?\s*([^;]+)\)?",
    re.I,
)
SINK_EXEC_RE = re.compile(
    r"\b(?:eval|assert|system|exec|passthru|shell_exec|popen|proc_open|file_put_contents|unserialize)\s*\((.*?)\)",
    re.I,
)
MAGIC_METHODS = re.compile(r"function\s+__(?:destruct|wakeup|toString|invoke|call|get|set)\s*\(", re.I)
SINKS_RE = re.compile(
    r"\b(?:eval|assert|system|exec|passthru|shell_exec|popen|proc_open|file_put_contents|unserialize|include|require)\b",
    re.I,
)
ENTRY_NAMES_RE = re.compile(
    r"(?:install|setup|admin|config|console|cron|index|init|server|tool|api|test|debug)\.php$", re.I
)
ENTRY_NAME_LIST = [
    "example", "examples", "demo", "demos", "sample", "samples",
    "tool", "tools", "admin", "public", "web", "install", "setup", "bin", "inc",
]

CATEGORIES = {
    "Direct Procedural Web Entry": [],
    "POP Gadget Chains (Deserialization)": [],
    "Controller / Action Vulnerability": [],
    "Command / Process Execution": [],
    "Arbitrary File Write / Template Injection": [],
    "SQL Injection in DB / ORM Layers": [],
}


# ── Mode: triage ──
def run_triage():
    """Full autonomous deep-triage across all packages."""
    queue_dir = DATA_DIR / "queue"
    queue_dir.mkdir(parents=True, exist_ok=True)
    dossiers_file = DATA_DIR / "HIGH_CONFIDENCE_TARGET_DOSSIERS.md"

    discovered_targets = []

    if not SCAN_CACHE.exists():
        print("[-] scan_cache not found")
        return

    for pkg_dir in sorted(SCAN_CACHE.iterdir()):
        if not pkg_dir.is_dir():
            continue

        pkg_folder_name = pkg_dir.name
        parts_name = pkg_folder_name.split("_")
        if len(parts_name) >= 3:
            pkg_name = "/".join(parts_name[:-1]).replace("_", "/")
            ver = parts_name[-1]
        else:
            pkg_name = pkg_folder_name
            ver = "latest"

        for php_file in pkg_dir.rglob("*.php"):
            rel_parts = [p.lower() for p in php_file.parts]
            rel_path = str(php_file.relative_to(pkg_dir))

            if "phpunit" in rel_parts or "tests" in rel_parts or "fixtures" in rel_parts:
                continue

            is_exposed = any(k in rel_parts for k in ENTRY_NAME_LIST) or php_file.name.lower() in [
                "index.php", "test.php", "getsource.php", "install.php", "setup.php", "admin.php",
            ]
            if not is_exposed:
                continue

            try:
                code_text = php_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = code_text.split("\n")
            has_input = bool(SRC_RE.search(code_text))

            for line_no, line in enumerate(lines, 1):
                s = line.strip()
                if not s or s.startswith(("//", "*", "#")):
                    continue

                m_read = SINK_READ_RE.search(s)
                if m_read:
                    read_target = m_read.group(1)
                    if SRC_RE.search(read_target) or any(
                        v in read_target for v in ["$file", "$path", "$url", "$f", "$src", "$page", "$view", "$template", "$doc"]
                    ):
                        discovered_targets.append({
                            "package_raw": pkg_folder_name,
                            "package_name": pkg_name,
                            "version": ver,
                            "type": "ARBITRARY_FILE_READ_LFI",
                            "file": rel_path,
                            "line": line_no,
                            "code": s[:130],
                            "has_input": has_input,
                        })

                m_exec = SINK_EXEC_RE.search(s)
                if m_exec:
                    exec_target = m_exec.group(1)
                    if SRC_RE.search(exec_target) or any(
                        v in exec_target for v in ["$cmd", "$code", "$data", "$pass", "$command", "$query", "$sql", "$payload"]
                    ):
                        discovered_targets.append({
                            "package_raw": pkg_folder_name,
                            "package_name": pkg_name,
                            "version": ver,
                            "type": "CODE_CMD_EXEC_DESER",
                            "file": rel_path,
                            "line": line_no,
                            "code": s[:130],
                            "has_input": has_input,
                        })

    print(f"[+] Discovered {len(discovered_targets)} actionable candidates")

    unique_dossiers = defaultdict(list)
    for t in discovered_targets:
        key = (t["package_name"], t["version"], t["file"])
        unique_dossiers[key].append(t)

    print(f"[+] Unique actionable file endpoints: {len(unique_dossiers)}")

    # Write dossiers
    dossier_entries = []
    count = 2
    for (p_name, p_ver, f_path), hits in sorted(unique_dossiers.items(), key=lambda x: -len(x[1])):
        count += 1
        top_hit = hits[0]
        dossier_entries.append(f"""
## {count}. `{p_name}:{p_ver}`

### Vulnerability Summary
- **Type**: {top_hit['type']}
- **Entry**: `/vendor/{p_name}/{f_path}`
- **Line**: {top_hit['line']}
- **Code**: `{top_hit['code']}`
""")

        # Publish task specs to queue
        for php_v in ["7.4.33", "8.4"]:
            task_id = f"task_{p_name.replace('/', '_')}_{p_ver}_{php_v}_{count}"
            task_spec = {
                "task_id": task_id,
                "package_name": p_name,
                "version": p_ver,
                "php_version": php_v,
                "endpoint": f"/vendor/{p_name}/{f_path}",
                "method": "GET",
                "vuln_type": top_hit["type"],
                "sample_code": top_hit["code"],
                "line": top_hit["line"],
            }
            (queue_dir / f"{task_id}.json").write_text(
                json.dumps(task_spec, indent=2, ensure_ascii=False), encoding="utf-8"
            )

    existing = dossiers_file.read_text(encoding="utf-8") if dossiers_file.exists() else "# Target Dossiers\n"
    dossiers_file.write_text(existing + "\n".join(dossier_entries), encoding="utf-8")
    print(f"[+] Published {len(unique_dossiers)} dossiers and queued tasks")


# ── Mode: categorize ──
def run_categorize():
    """Categorize vulnerabilities by type across all packages."""
    results_by_pkg = defaultdict(lambda: defaultdict(list))

    if not SCAN_CACHE.exists():
        print("[-] scan_cache not found")
        return

    for pkg_dir in SCAN_CACHE.iterdir():
        if not pkg_dir.is_dir():
            continue
        pkg_name = pkg_dir.name

        for php_file in pkg_dir.rglob("*.php"):
            parts = [p.lower() for p in php_file.parts]
            if any(k in parts for k in ["fixtures", "tests", "test"]):
                continue
            try:
                content = php_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            rel_path = str(php_file.relative_to(pkg_dir))

            # Procedural Entry Point with Sinks
            if ENTRY_NAMES_RE.search(php_file.name):
                for line_no, line in enumerate(content.split("\n"), 1):
                    if SINKS_RE.search(line) and not line.strip().startswith(("//", "*", "#")):
                        results_by_pkg[pkg_name]["Direct Procedural Web Entry"].append({
                            "file": rel_path, "line": line_no, "code": line.strip()[:120],
                        })

            # POP Gadget Chains
            if MAGIC_METHODS.search(content) and SINKS_RE.search(content):
                in_magic = False
                for line_no, line in enumerate(content.split("\n"), 1):
                    if MAGIC_METHODS.search(line):
                        in_magic = True
                    if in_magic and SINKS_RE.search(line) and not line.strip().startswith(("//", "*", "#")):
                        results_by_pkg[pkg_name]["POP Gadget Chains (Deserialization)"].append({
                            "file": rel_path, "line": line_no, "code": line.strip()[:120],
                        })
                        in_magic = False

            # Controller / Action Vulnerability
            if any(k in rel_path.lower() for k in ["controller", "command", "handler", "action", "model"]):
                for line_no, line in enumerate(content.split("\n"), 1):
                    if SINKS_RE.search(line) and not line.strip().startswith(("//", "*", "#")):
                        results_by_pkg[pkg_name]["Controller / Action Vulnerability"].append({
                            "file": rel_path, "line": line_no, "code": line.strip()[:120],
                        })

    # Summary
    summary_list = []
    for pkg, cat_dict in results_by_pkg.items():
        total = sum(len(v) for v in cat_dict.values())
        if total > 0:
            summary_list.append({
                "package": pkg,
                "total": total,
                "categories": {k: len(v) for k, v in cat_dict.items() if v},
            })

    summary_list.sort(key=lambda x: -x["total"])
    print(f"Total packages with actionable vulns: {len(summary_list)}\n")
    print("--- TOP 30 ACTIONABLE PACKAGES ---")
    for s in summary_list[:30]:
        cats = ", ".join(f"{k}: {v}" for k, v in s["categories"].items())
        print(f"  {s['package']:45} | {s['total']:3d} | {cats}")

    out_file = DATA_DIR / "actionable_exploit_vectors.json"
    out_file.write_text(json.dumps(dict(results_by_pkg), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[+] Saved to {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified triage tool")
    parser.add_argument("--mode", choices=["triage", "categorize"], required=True)
    args = parser.parse_args()

    if args.mode == "triage":
        run_triage()
    else:
        run_categorize()
