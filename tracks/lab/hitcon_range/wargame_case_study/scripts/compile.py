#!/usr/bin/env python3
"""
Consolidated compilation script.
Replaces: compile_50_attack_vectors, compile_all_dossiers, compile_full_catalog

Usage:
    python scripts/compile.py --format vectors    # 50-vector attack matrix
    python scripts/compile.py --format dossiers   # Package security dossiers
    python scripts/compile.py --format catalog    # Full security catalog
"""
import sys
import json
import re
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.paths import SCAN_CACHE, RESULTS_DIR, DATA_DIR


# --- 50 Attack Vector Taxonomy ---
TAXONOMY_50 = {
    "P01_INSTALLER_SETUP": re.compile(r"(?:install|setup|wizard|configure|build)\.php$", re.I),
    "P02_DEMO_EXAMPLE": re.compile(r"(?:demo|demos|example|examples|sample|samples)/.*?\.php$", re.I),
    "P03_ADMIN_BACKEND": re.compile(r"(?:admin|administrator|backend|manage|dashboard)/.*?\.php$|admin\.php$", re.I),
    "P04_TEST_DEBUG_PROBE": re.compile(r"(?:test|tests|debug|probe|bench|benchmark|check|diag|doctor)\.php$", re.I),
    "P05_API_WEBHOOK_ENDPOINT": re.compile(r"(?:api|webhook|webhooks|callback|notify|gateway|endpoint|ipn)\.php$", re.I),
    "P06_TOOL_UTILITY_SCRIPT": re.compile(r"(?:tool|tools|util|utils|scripts|bin|misc)/.*?\.php$", re.I),
    "P07_STANDALONE_INDEX": re.compile(r"(?:public|web|docroot|html|htdocs|ui)/index\.php$", re.I),
    "P08_UPLOAD_DOWNLOAD_HANDLER": re.compile(r"(?:upload|uploader|download|fetch|attachment|export|import)\.php$", re.I),
    "P09_VIEW_SOURCE_PREVIEW": re.compile(r"(?:getsource|source|view|show|preview|render|display)\.php$", re.I),
    "P10_MOCK_SERVER_EMULATOR": re.compile(r"(?:mock|server|stub|fake|emulator|simulator)/.*?\.php$|server\.php$", re.I),
    "P11_FILE_PUT_CONTENTS_INJECTION": re.compile(r"\bfile_put_contents\s*\(", re.I),
    "P12_FWRITE_STREAM_CORRUPTION": re.compile(r"\b(?:fwrite|fputs)\s*\(", re.I),
    "P13_DYNAMIC_REQUIRE_LFI": re.compile(r"\b(?:require|require_once)\s*\(?\s*\$", re.I),
    "P14_DYNAMIC_INCLUDE_LFI": re.compile(r"\b(?:include|include_once)\s*\(?\s*\$", re.I),
    "P15_HIGHLIGHT_FILE_SOURCE_LEAK": re.compile(r"\b(?:highlight_file|show_source)\s*\(", re.I),
    "P16_READFILE_ARBITRARY_READ": re.compile(r"\b(?:readfile|file_get_contents)\s*\(\s*\$", re.I),
    "P17_MOVE_UPLOADED_FILE_ESCAPE": re.compile(r"\bmove_uploaded_file\s*\(", re.I),
    "P18_UNLINK_ARBITRARY_DELETE": re.compile(r"\bunlink\s*\(\s*\$", re.I),
    "P19_TOUCH_CHMOD_PERM_TAMPER": re.compile(r"\b(?:chmod|chown|touch)\s*\(\s*\$", re.I),
    "P20_ZIP_ARCHIVE_TRAVERSAL": re.compile(r"\b(?:ZipArchive|PharData|extractTo)\b", re.I),
    "P21_EVAL_DYNAMIC_CODE": re.compile(r"\beval\s*\(", re.I),
    "P22_ASSERT_STRING_EVAL": re.compile(r"\bassert\s*\(\s*[\"']", re.I),
    "P23_PREG_REPLACE_E_MODIFIER": re.compile(r"preg_replace\s*\(\s*['\"].*?/e[a-z]*['\"]", re.I),
    "P24_CREATE_FUNCTION_RCE": re.compile(r"\bcreate_function\s*\(", re.I),
    "P25_VARIABLE_FUNCTION_DISPATCH": re.compile(r"\$[a-zA-Z0-9_]+\s*\(\s*\$", re.I),
    "P26_CALL_USER_FUNC_ARRAY": re.compile(r"\b(?:call_user_func|call_user_func_array)\s*\(\s*\$", re.I),
    "P27_USORT_ARRAY_CALLBACK": re.compile(r"\b(?:usort|uasort|uksort|array_walk|array_map|array_filter)\s*\([^,]+,\s*\$", re.I),
    "P28_REFLECTION_METHOD_INVOKE": re.compile(r"\bReflectionMethod.*?->invoke", re.I),
    "P29_REGISTER_SHUTDOWN_FUNCTION": re.compile(r"\bregister_shutdown_function\s*\(", re.I),
    "P30_OB_START_CALLBACK_INJECTION": re.compile(r"\bob_start\s*\(\s*\$", re.I),
    "P31_SYSTEM_COMMAND_EXEC": re.compile(r"\bsystem\s*\(", re.I),
    "P32_EXEC_SHELL_EXEC": re.compile(r"\b(?:exec|shell_exec)\s*\(", re.I),
    "P33_PASSTHRU_RAW_OUTPUT": re.compile(r"\bpassthru\s*\(", re.I),
    "P34_POPEN_PROC_OPEN_PIPES": re.compile(r"\b(?:popen|proc_open)\s*\(", re.I),
    "P35_BACKTICK_COMMAND_INTERP": re.compile(r"`[^`\$]*\$[^`]+`", re.I),
    "P36_PCNTL_EXEC_FORK": re.compile(r"\bpcntl_exec\s*\(", re.I),
    "P37_MAIL_EXTRA_PARAMS_ESCAPE": re.compile(r"\bmail\s*\([^,]+,[^,]+,[^,]+,[^,]+,\s*\$", re.I),
    "P38_MB_SEND_MAIL_ESCAPE": re.compile(r"\bmb_send_mail\s*\([^,]+,[^,]+,[^,]+,[^,]+,\s*\$", re.I),
    "P39_MYSQLDUMP_BACKUP_SINK": re.compile(r"(?:mysqldump|pg_dump|tar|gzip|unzip)\s+.*?\$", re.I),
    "P40_FFMPEG_IMAGICK_CLI_WRAPPER": re.compile(r"(?:ffmpeg|convert|gs|pdftoppm)\s+.*?\$", re.I),
    "P41_UNSERIALIZE_POP_GADGET": re.compile(r"\bunserialize\s*\(", re.I),
    "P42_MAGIC_METHOD_DESTRUCT_SINK": re.compile(r"function\s+__destruct\s*\(", re.I),
    "P43_MAGIC_METHOD_WAKEUP_TOSTRING": re.compile(r"function\s+__(?:wakeup|toString|invoke)\s*\(", re.I),
    "P44_RAW_SQL_CONCATENATION": re.compile(r"(?:SELECT|INSERT|UPDATE|DELETE|UNION)\s+.*?\$[a-zA-Z0-9_]+", re.I),
    "P45_SQLITE_ATTACH_DB_WRITE": re.compile(r"ATTACH\s+DATABASE|\.open|\.dump", re.I),
    "P46_CURL_SSRF_REDIRECT": re.compile(r"CURLOPT_URL\s*,\s*\$|\bcurl_init\s*\(\s*\$", re.I),
    "P47_SOAP_CLIENT_SSRF_XXE": re.compile(r"\bSoapClient\b", re.I),
    "P48_SIMPLEXML_DOM_XXE": re.compile(r"\b(?:simplexml_load_string|simplexml_load_file|DOMDocument)\b", re.I),
    "P49_EXTRACT_VARIABLE_OVERWRITE": re.compile(r"\bextract\s*\(\s*\$_(?:GET|POST|REQUEST)", re.I),
    "P50_TYPE_JUGGLING_AUTH_BYPASS": re.compile(r"(?:md5|sha1|hash)\s*\([^)]+\)\s*==\s*", re.I),
}


def _scan_php_file_vectors(php_file, pkg_dir, pkg_summary, vector_hits):
    parts = [p.lower() for p in php_file.parts]
    if any(ex in parts for ex in ["phpunit", "tests", "fixtures"]):
        return
    try:
        content = php_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    rel_file = str(php_file.relative_to(pkg_dir))
    tax_keys = list(TAXONOMY_50.keys())
    for vec_id in tax_keys[:10]:
        if TAXONOMY_50[vec_id].search(rel_file):
            pkg_summary[pkg_dir.name][vec_id] += 1
            vector_hits[vec_id][pkg_dir.name].append({"file": rel_file, "line": 1})

    for line_no, line in enumerate(content.split("\n"), 1):
        s = line.strip()
        if not s or s.startswith(("//", "*", "#")):
            continue
        for vec_id in tax_keys[10:]:
            if TAXONOMY_50[vec_id].search(s):
                pkg_summary[pkg_dir.name][vec_id] += 1
                if len(vector_hits[vec_id][pkg_dir.name]) < 10:
                    vector_hits[vec_id][pkg_dir.name].append({
                        "file": rel_file, "line": line_no, "code": s[:120]
                    })


def compile_vectors():
    """Compile 50-vector attack matrix across all cached packages."""
    print("[*] Compiling 50 Attack Vector Matrix...")

    vector_hits = defaultdict(lambda: defaultdict(list))
    pkg_summary = defaultdict(lambda: defaultdict(int))

    if not SCAN_CACHE.exists():
        print("[-] scan_cache not found")
        return

    for pkg_dir in SCAN_CACHE.iterdir():
        if not pkg_dir.is_dir():
            continue
        for php_file in pkg_dir.rglob("*.php"):
            _scan_php_file_vectors(php_file, pkg_dir, pkg_summary, vector_hits)

    vector_counts = {}
    for vec_id in sorted(TAXONOMY_50.keys()):
        pkgs = len(vector_hits[vec_id])
        instances = sum(len(h) for h in vector_hits[vec_id].values())
        vector_counts[vec_id] = {"packages": pkgs, "instances": instances}
        print(f"  [{vec_id:34}] Packages: {pkgs:3d} | Instances: {instances:5d}")

    out_file = DATA_DIR / "matrix_50_attack_vectors.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps({
        "vector_summary": vector_counts,
        "package_breakdown": dict(pkg_summary),
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[+] Saved to: {out_file}")


def compile_catalog():
    """Compile full security catalog for all packages."""
    pkgs_file = RESULTS_DIR / "all_packages.json"
    findings_file = RESULTS_DIR / "global_4701_sast_findings.json"
    if not findings_file.exists():
        findings_file = RESULTS_DIR / "comprehensive_sast_findings.json"

    all_pkgs = json.loads(pkgs_file.read_text(encoding="utf-8")) if pkgs_file.exists() else []
    findings = json.loads(findings_file.read_text(encoding="utf-8")) if findings_file.exists() else []

    findings_by_pkg = defaultdict(list)
    for f in findings:
        findings_by_pkg[f["package"]].append(f)

    unique_pkgs = {}
    for p in all_pkgs:
        key = (p["name"], p["version"])
        if key not in unique_pkgs:
            unique_pkgs[key] = {"name": p["name"], "version": p["version"], "php_versions": set()}
        unique_pkgs[key]["php_versions"].add(p.get("php_version", "7.4.33"))

    print(f"[*] Cataloging {len(unique_pkgs)} packages with {len(findings)} findings...")

    catalog = []
    for (name, ver), info in sorted(unique_pkgs.items()):
        hits = findings_by_pkg.get(f"{name}:{ver}", []) or findings_by_pkg.get(name, [])
        sev_counts = defaultdict(int)
        cat_counts = defaultdict(int)
        for h in hits:
            sev_counts[h.get("severity", "MEDIUM")] += 1
            cat_counts[h.get("category", "General")] += 1

        risk = "CRITICAL" if sev_counts["CRITICAL"] > 0 else (
            "HIGH" if sev_counts["HIGH"] > 0 else (
                "MEDIUM" if sev_counts["MEDIUM"] > 0 else "LOW"))

        catalog.append({
            "package_name": name, "version": ver,
            "php_versions": sorted(list(info["php_versions"])),
            "risk_level": risk, "total_findings": len(hits),
            "severity_breakdown": dict(sev_counts),
            "category_breakdown": dict(cat_counts),
        })

    out_file = DATA_DIR / "complete_package_security_catalog.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Catalog saved to: {out_file}")


def compile_dossiers():
    """Compile package security dossiers."""
    from scripts.triage import run_triage
    run_triage()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Consolidated compilation script")
    parser.add_argument("--format", required=True, choices=["vectors", "dossiers", "catalog"])
    args = parser.parse_args()

    if args.format == "vectors":
        compile_vectors()
    elif args.format == "catalog":
        compile_catalog()
    elif args.format == "dossiers":
        compile_dossiers()
    else:
        print(f"[-] Format '{args.format}' not recognized")


if __name__ == "__main__":
    main()
