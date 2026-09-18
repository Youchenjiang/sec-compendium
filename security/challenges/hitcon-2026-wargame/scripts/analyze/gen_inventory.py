#!/usr/bin/env python3
"""
Generate a comprehensive package inventory CSV for HITCON 2026 Wargame.
Cross-references: SAST scan results, platform solved packages, exploit scripts, scan cache.
"""
import json
import csv
from pathlib import Path
from collections import defaultdict
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.paths import SCAN_CACHE, RESULTS_DIR
OUTPUT_CSV = RESULTS_DIR / "package_inventory.csv"
OUTPUT_MD = RESULTS_DIR / "package_inventory.md"

ACTIONABLE_TYPES = {
    "system/exec/passthru invocation",
    "Direct eval() execution",
    "preg_replace /e modifier",
    "file_put_contents file write",
    "Dynamic include / require",
    "Variable function call with variable",
    "create_function() deprecated RCE",
    "Backtick shell execution",
    "unserialize() invocation",
    "SQL query with string concatenation",
    "Dynamic file read (file_get_contents/readfile)",
}

PRIORITY_ORDER = {
    "DONE": 0, "P1-CRIT": 1, "P1-SUPERGLOBAL": 2, "P1-NEED-DL": 3,
    "P2-WEB": 4, "P2-HIGH": 5, "P3-HIGH-NC": 6, "P4-MED": 7, "-": 8
}


def _to_composer(scan_name: str) -> str:
    """Convert scan_cache name to composer name. e.g., owasp_phprbac_2.0.0 -> owasp/phprbac"""
    parts = scan_name.rsplit("_", 1)
    if len(parts) == 2:
        return parts[0].replace("_", "/")
    return scan_name.replace("_", "/")


def _load_data():
    sast_path = RESULTS_DIR / "comprehensive_sast_findings.json"
    solved_path = RESULTS_DIR / "all_solved.json"

    if not sast_path.exists() or not solved_path.exists():
        print(f"[!] Missing required findings data in {RESULTS_DIR}:")
        if not sast_path.exists():
            print(f"    - {sast_path.name} not found")
        if not solved_path.exists():
            print(f"    - {solved_path.name} not found")
        print("[!] Run scan tools and fetch solved challenges first before generating inventory.")
        return None, None

    with open(sast_path, encoding="utf-8") as f:
        sast = json.load(f)
    with open(solved_path, encoding="utf-8") as f:
        solved_list = json.load(f)

    return sast, solved_list


def _build_solved_lookup(solved_list):
    solved_lookup = {}
    for p in solved_list:
        name = p["name"]
        ver = p["version"]
        php = p.get("php_version", "")
        key = f"{name}:{ver}"
        if key not in solved_lookup:
            solved_lookup[key] = {}
        solved_lookup[key][php] = {
            "solve_count": p.get("successful_exploit_count"),
            "attempt_count": p.get("attempt_count"),
            "id": p.get("id", ""),
        }
    return solved_lookup


def _build_sast_by_pkg(sast):
    sast_by_pkg = defaultdict(lambda: {
        "total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0,
        "types": set(), "files": set(), "has_superglobal": False,
        "pkg_scan_name": "",
    })

    for item in sast:
        pkg_scan = item["package"]
        composer = _to_composer(pkg_scan)
        info = sast_by_pkg[composer]
        info["total"] += 1
        info["pkg_scan_name"] = pkg_scan

        sev = item.get("severity", "UNKNOWN")
        if sev == "CRITICAL":
            info["critical"] += 1
        elif sev == "HIGH":
            info["high"] += 1
        elif sev == "MEDIUM":
            info["medium"] += 1
        elif sev == "LOW":
            info["low"] += 1

        info["types"].add(item.get("type", ""))
        info["files"].add(item.get("file", ""))
        if item.get("has_superglobal"):
            info["has_superglobal"] = True

    return sast_by_pkg


def _get_cache_dirs():
    cache_dirs = set()
    if SCAN_CACHE.exists():
        for d in SCAN_CACHE.iterdir():
            if d.is_dir():
                cache_dirs.add(d.name)
    return cache_dirs


def _is_cached(composer_name, pkg_scan_name, cache_dirs):
    safe = composer_name.replace("/", "_")
    for c in cache_dirs:
        if safe in c:
            return True
    return bool(pkg_scan_name and pkg_scan_name in cache_dirs)


def _get_exploit_pkgs():
    exploit_pkgs = set()
    exploit_dir = RESULTS_DIR / "exploits_solved"
    if exploit_dir.exists():
        for d in exploit_dir.iterdir():
            if d.is_dir():
                composer = d.name.replace("_", "/", 1)
                exploit_pkgs.add(composer)
    return exploit_pkgs


def _determine_priority(has_exploit, info, cached, has_web_entry):
    if has_exploit:
        return "DONE"
    if info["critical"] > 0 and cached:
        return "P1-CRIT"
    if info["critical"] > 0 and not cached:
        return "P1-NEED-DL"
    if info["high"] > 0 and info["has_superglobal"]:
        return "P1-SUPERGLOBAL"
    if info["high"] > 0 and cached and has_web_entry:
        return "P2-WEB"
    if info["high"] > 0 and cached:
        return "P2-HIGH"
    if info["high"] > 0:
        return "P3-HIGH-NC"
    if info["medium"] > 0:
        return "P4-MED"
    return "-"


def _build_package_row(composer, sast_by_pkg, solved_lookup, cache_dirs, exploit_pkgs):  # skipcq: PY-R1000
    info = sast_by_pkg.get(composer, {
        "total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0,
        "types": set(), "files": set(), "has_superglobal": False,
        "pkg_scan_name": "",
    })

    solved_key = None
    solve_count = ""
    attempt_count = ""
    php_versions = []
    for key, php_info in solved_lookup.items():
        if key.startswith(composer + ":"):
            solved_key = key
            for php, pdata in php_info.items():
                php_versions.append(php)
                if pdata["solve_count"] is not None:
                    solve_count = str(pdata["solve_count"])
                if pdata["attempt_count"] is not None:
                    attempt_count = str(pdata["attempt_count"])

    is_solved = solved_key is not None
    cached = _is_cached(composer, info["pkg_scan_name"], cache_dirs)
    has_exploit = composer in exploit_pkgs

    has_web_entry = any(
        k in f.lower()
        for f in info["files"]
        for k in ["install", "setup", "index", "admin", "config", "app"]
    )
    priority = _determine_priority(has_exploit, info, cached, has_web_entry)

    return {
        "package": composer,
        "cached": "Y" if cached else "",
        "solved": "Y" if is_solved else "",
        "solve_count": solve_count,
        "attempt_count": attempt_count,
        "php_versions": ", ".join(php_versions),
        "sast_total": info["total"],
        "sast_critical": info["critical"],
        "sast_high": info["high"],
        "sast_medium": info["medium"],
        "sast_low": info["low"],
        "has_superglobal": "Y" if info["has_superglobal"] else "",
        "actionable_types": "; ".join(sorted(info["types"] & ACTIONABLE_TYPES)),
        "key_files": "; ".join(sorted(info["files"])[:3]),
        "exploit_script": "DONE" if has_exploit else "",
        "priority": priority,
    }


def _write_csv(rows):
    fieldnames = [
        "package", "cached", "solved", "solve_count", "attempt_count", "php_versions",
        "sast_total", "sast_critical", "sast_high", "sast_medium", "sast_low",
        "has_superglobal", "actionable_types", "key_files",
        "exploit_script", "priority",
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[+] CSV written to {OUTPUT_CSV} ({len(rows)} packages)")


def _write_markdown(rows):  # skipcq: PY-R1000
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# HITCON 2026 Wargame - 套件庫存總覽\n\n")
        f.write(f"> 共 {len(rows)} 個套件 | 掃描發現 43,924 項 | 已下載 {sum(1 for r in rows if r['cached'])} 個 | 已 solved {sum(1 for r in rows if r['solved'])} 個 | 已有 exploit {sum(1 for r in rows if r['exploit_script'])} 個\n\n")

        f.write("## 📊 統計摘要\n\n")
        f.write("| 狀態 | 數量 |\n|------|------|\n")
        f.write(f"| 已有 Exploit ✅ | {sum(1 for r in rows if r['exploit_script'])} |\n")
        f.write(f"| P1-CRIT (已下載, 有 critical) | {sum(1 for r in rows if r['priority'] == 'P1-CRIT')} |\n")
        f.write(f"| P1-SUPERGLOBAL (有 superglobal 輸入) | {sum(1 for r in rows if r['priority'] == 'P1-SUPERGLOBAL')} |\n")
        f.write(f"| P1-NEED-DL (有 critical, 未下載) | {sum(1 for r in rows if r['priority'] == 'P1-NEED-DL')} |\n")
        f.write(f"| P2-WEB (已下載, 有 web 入口) | {sum(1 for r in rows if r['priority'] == 'P2-WEB')} |\n")
        f.write(f"| P2-HIGH (已下載, 有 high) | {sum(1 for r in rows if r['priority'] == 'P2-HIGH')} |\n")
        f.write(f"| P3-HIGH-NC (有 high, 未下載) | {sum(1 for r in rows if r['priority'] == 'P3-HIGH-NC')} |\n")
        f.write(f"| P4-MED (只有 medium) | {sum(1 for r in rows if r['priority'] == 'P4-MED')} |\n")
        f.write(f"| 無 findings | {sum(1 for r in rows if r['priority'] == '-')} |\n\n")

        f.write("## 🎯 高優先套件（需要生成 exploit）\n\n")
        f.write("| 套件 | Cached | Solved | Solves | Crit | High | Global | Actionable Types | Exploit | Priority |\n")
        f.write("|------|--------|--------|--------|------|------|--------|-----------------|---------|----------|\n")

        for r in rows:
            if r["priority"] in ("DONE", "P1-CRIT", "P1-SUPERGLOBAL", "P1-NEED-DL", "P2-WEB"):
                f.write(f"| {r['package']} | {r['cached']} | {r['solved']} | {r['solve_count']} | {r['sast_critical']} | {r['sast_high']} | {r['has_superglobal']} | {r['actionable_types'][:60]} | {r['exploit_script']} | {r['priority']} |\n")

        f.write("\n\n")
        f.write("## 📋 完整套件清單\n\n")
        f.write("| # | Package | Cached | Solved | Solves | Crit | High | Med | Low | Global | Exploit | Priority |\n")
        f.write("|---|---------|--------|--------|--------|------|------|-----|-----|--------|---------|----------|\n")

        for i, r in enumerate(rows, 1):
            f.write(f"| {i} | {r['package']} | {r['cached']} | {r['solved']} | {r['solve_count']} | {r['sast_critical']} | {r['sast_high']} | {r['sast_medium']} | {r['sast_low']} | {r['has_superglobal']} | {r['exploit_script']} | {r['priority']} |\n")

        f.write("\n\n")
        f.write("## ✅ Exploit 建立進度\n\n")
        f.write("| 套件 | Version | PHP | Vuln Type | Exploit Path | Status |\n")
        f.write("|------|---------|-----|-----------|-------------|--------|\n")

        manifest_path = RESULTS_DIR / "exploits_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, encoding="utf-8") as mf:
                manifest = json.load(mf)
            seen = set()
            for m in manifest:
                key = f"{m['package']}:{m.get('php_version', '')}"
                if key in seen:
                    continue
                seen.add(key)
                status = m.get("status", "testing")
                f.write(f"| {m['package']} | {m.get('version', '')} | {m.get('php_version', '')} | {m.get('vuln_type', '')} | {m.get('exploit_path', '')} | {status} |\n")

    print(f"[+] MD written to {OUTPUT_MD}")


def main():
    sast, solved_list = _load_data()
    if sast is None:
        return 1

    solved_lookup = _build_solved_lookup(solved_list)
    sast_by_pkg = _build_sast_by_pkg(sast)
    cache_dirs = _get_cache_dirs()
    exploit_pkgs = _get_exploit_pkgs()

    all_packages = {key.rsplit(":", 1)[0] for key in solved_lookup} | set(sast_by_pkg.keys())
    rows = [
        _build_package_row(composer, sast_by_pkg, solved_lookup, cache_dirs, exploit_pkgs)
        for composer in sorted(all_packages)
    ]
    rows.sort(key=lambda r: (PRIORITY_ORDER.get(r["priority"], 9), -r["sast_critical"], -r["sast_high"], r["package"]))

    _write_csv(rows)
    _write_markdown(rows)

    print("\nSummary:")
    print(f"  Total packages: {len(rows)}")
    print(f"  With exploit:   {sum(1 for r in rows if r['exploit_script'])}")
    print(f"  P1-CRIT:        {sum(1 for r in rows if r['priority'] == 'P1-CRIT')}")
    print(f"  P1-SUPERGLOBAL: {sum(1 for r in rows if r['priority'] == 'P1-SUPERGLOBAL')}")
    print(f"  P1-NEED-DL:     {sum(1 for r in rows if r['priority'] == 'P1-NEED-DL')}")
    print(f"  P2-WEB:         {sum(1 for r in rows if r['priority'] == 'P2-WEB')}")
    print(f"  P2-HIGH:        {sum(1 for r in rows if r['priority'] == 'P2-HIGH')}")
    print(f"  Cached:         {sum(1 for r in rows if r['cached'])}")
    print(f"  Solved:         {sum(1 for r in rows if r['solved'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
