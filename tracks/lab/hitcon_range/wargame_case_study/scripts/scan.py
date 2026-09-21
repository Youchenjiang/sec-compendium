#!/usr/bin/env python3
"""
Consolidated vulnerability scanner.
Replaces: scan_all_packages, scan_local_266, scan_solved, scan_targeted,
           batch_scan, audit_all_4701_packages

Usage:
    python scripts/scan.py --scope local        # Scan local 266 cached packages
    python scripts/scan.py --scope all          # Scan all packages via Docker
    python scripts/scan.py --scope solved       # Scan solved packages only
    python scripts/scan.py --scope targeted     # Scan specific targeted packages
    python scripts/scan.py --scope batch [N]    # Batch scan top N packages
    python scripts/scan.py --scope global       # Global audit of all 4701 packages
    python scripts/scan.py --scope deep         # Deep scan with data-flow analysis
    python scripts/scan.py --scope docker PKG VER PHP  # Scan specific package in Docker
"""
import sys
import json
import re
import subprocess
import time
import urllib.request
import tarfile
import io
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.paths import SCAN_CACHE, RESULTS_DIR
from lib.scanner_rules import BROAD_RULES
from lib.scanner_utils import has_superglobal


# --- Dangerous sink patterns ---
DANGEROUS_SINKS = {
    "Code Execution (eval/assert)": r'\b(?:eval|assert)\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE|SERVER)',
    "Command Injection (exec/system)": r'\b(?:system|exec|passthru|shell_exec|popen|proc_open)\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE|SERVER)',
    "Direct File Put Contents": r'file_put_contents\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)',
    "Direct Unserialize": r'unserialize\s*\(.*\$_(?:GET|POST|REQUEST|COOKIE)',
    "Direct LFI / Include": r'\b(?:include|require|include_once|require_once)\s*\(?.*\$_(?:GET|POST|REQUEST|COOKIE)',
    "preg_replace /e": r"preg_replace\s*\(\s*['\"].*?/e[a-z]*['\"]",
}


def scan_package_dir(pkg_dir):  # skipcq: PY-R1000
    """Scan a single cached package directory for vulnerabilities."""
    findings = []
    vendor_dir = pkg_dir / "vendor"
    scan_root = vendor_dir if vendor_dir.exists() else pkg_dir

    for php_file in scan_root.rglob("*.php"):
        parts = [p.lower() for p in php_file.parts]
        if any(ex in parts for ex in ["composer", "tests", "test", "fixtures", "phpstan", "rector"]):
            continue
        if php_file.name == "autoload.php":
            continue

        try:
            content = php_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        lines = content.split("\n")
        rel_path = str(php_file.relative_to(pkg_dir))

        # Single-line pattern matching
        for idx, line in enumerate(lines, 1):
            s = line.strip()
            if not s or s.startswith(("//", "#", "*")):
                continue
            for name, pattern in DANGEROUS_SINKS.items():
                if re.search(pattern, s, re.IGNORECASE):
                    findings.append({
                        "package": pkg_dir.name,
                        "type": name,
                        "severity": "CRITICAL" if "Execution" in name or "Injection" in name else "HIGH",
                        "file": rel_path,
                        "line": idx,
                        "code": s[:120],
                    })

        # Multi-line taint: $_INPUT -> file_put_contents
        if has_superglobal(content) and "file_put_contents" in content:
            matches = re.finditer(
                r'(\$[a-zA-Z0-9_]+\s*=\s*[^;]*\$_(?:GET|POST|REQUEST)[\s\S]{1,500}?file_put_contents\s*\([^;]+\))',
                content,
            )
            for m in matches:
                line_no = content[:m.start()].count('\n') + 1
                findings.append({
                    "package": pkg_dir.name,
                    "type": "Tainted File Write / Code Injection",
                    "severity": "HIGH",
                    "file": rel_path,
                    "line": line_no,
                    "code": m.group(1).replace('\n', ' ')[:140],
                })

        # Standalone entry point detection
        lower_name = php_file.name.lower()
        if any(k in lower_name for k in ["install.php", "setup.php", "config.php", "upload.php", "admin.php"]) and any(sg in content for sg in ["$_GET", "$_POST", "$_REQUEST"]):
            for idx, line in enumerate(lines, 1):
                if any(sg in line for sg in ["$_GET", "$_POST", "$_REQUEST"]):
                    findings.append({
                        "package": pkg_dir.name,
                        "type": "Standalone Procedural Web Entry Point",
                        "severity": "MEDIUM",
                        "file": rel_path,
                        "line": idx,
                        "code": f"Procedural script {php_file.name} taking HTTP inputs directly",
                    })
                    break

    return findings


def scope_local(filter_names=None):
    """Scan locally cached packages (optionally filtered by names)."""
    if not SCAN_CACHE.exists():
        print("[-] scan_cache directory does not exist.")
        return

    packages = [p for p in SCAN_CACHE.iterdir() if p.is_dir()]
    if filter_names:
        packages = [p for p in packages if any(f.lower() in p.name.lower() for f in filter_names)]
    print(f"[*] Scanning {len(packages)} cached packages...")

    all_findings = []
    for idx, pkg_dir in enumerate(packages, 1):
        findings = scan_package_dir(pkg_dir)
        all_findings.extend(findings)
        if findings:
            print(f"[{idx}/{len(packages)}] [+] {pkg_dir.name}: {len(findings)} findings")

    out_file = RESULTS_DIR / "comprehensive_266_findings.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_findings, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Total findings: {len(all_findings)}")
    print(f"[+] Results saved to: {out_file}")


def scope_deep():
    """Deep scan with multi-line data-flow analysis."""
    from lib.scanner import Scanner
    scanner = Scanner(deep=True)

    if not SCAN_CACHE.exists():
        print("[-] scan_cache directory does not exist.")
        return

    packages = [p for p in SCAN_CACHE.iterdir() if p.is_dir()]
    print(f"[*] Deep scanning {len(packages)} packages...")

    all_results = {}
    for idx, pkg_dir in enumerate(packages, 1):
        findings = scanner.scan_directory(pkg_dir)
        if findings:
            all_results[pkg_dir.name] = findings
            print(f"[{idx}/{len(packages)}] [+] {pkg_dir.name}: {len(findings)} findings")

    out_file = RESULTS_DIR / "deep_scan_findings.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    summary = scanner.get_summary()
    print(f"\n[+] Total findings: {summary['total']}")
    print(f"[+] Results saved to: {out_file}")


def scope_global():
    """Global audit of all 4701 packages via GitHub tarballs."""
    pkgs_file = RESULTS_DIR / "all_packages.json"
    if not pkgs_file.exists():
        print("[-] all_packages.json missing")
        return

    all_pkgs = json.loads(pkgs_file.read_text(encoding="utf-8"))
    unique_pkgs = {}
    for p in all_pkgs:
        unique_pkgs[(p["name"], p["version"])] = p

    pkg_list = list(unique_pkgs.values())
    print(f"[*] GLOBAL SCANNER: {len(pkg_list)} packages, 32 threads")

    def fetch_and_audit(pkg):
        name, ver = pkg["name"], pkg["version"]
        if "/" not in name:
            return []
        vendor, repo = name.split("/", 1)
        for tag in [f"v{ver}", ver, f"v.{ver}", f"{ver}-stable"]:
            url = f"https://github.com/{vendor}/{repo}/archive/refs/tags/{tag}.tar.gz"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=12) as resp:  # skipcq: BAN-B310
                    if resp.status == 200:
                        return _audit_tarball(resp.read(), f"{name}:{ver}")
            except Exception:
                continue
        return []

    t0 = time.time()
    total_findings = []
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(fetch_and_audit, pkg): pkg for pkg in pkg_list}
        for i, future in enumerate(as_completed(futures), 1):
            try:
                total_findings.extend(future.result())
            except Exception:
                pass
            if i % 100 == 0:
                print(f"[{i}/{len(pkg_list)}] {len(total_findings)} findings so far")

    out_file = RESULTS_DIR / "global_4701_sast_findings.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(total_findings, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Global audit complete in {time.time() - t0:.1f}s")
    print(f"[+] {len(total_findings)} findings across {len(pkg_list)} packages")


def _audit_tarball(raw_bytes, pkg_name):
    findings = []
    try:
        with tarfile.open(fileobj=io.BytesIO(raw_bytes), mode="r:*") as tar:
            for member in tar.getmembers():
                if not member.name.endswith(".php"):
                    continue
                parts = [p.lower() for p in member.name.split("/")]
                if any(ex in parts for ex in ["tests", "test", "fixtures"]):
                    continue
                f = tar.extractfile(member)
                if not f:
                    continue
                try:
                    content = f.read().decode("utf-8", errors="ignore")
                except Exception:
                    continue
                for idx, line in enumerate(content.split("\n"), 1):
                    s = line.strip()
                    if not s or s.startswith(("//", "#", "*")):
                        continue
                    for rule in BROAD_RULES:
                        if rule.search(s):
                            findings.append({
                                "package": pkg_name,
                                "category": rule.category,
                                "rule_id": rule.id,
                                "type": rule.name,
                                "severity": rule.severity,
                                "file": member.name.split("/")[-1],
                                "path": member.name,
                                "line": idx,
                                "code": s[:120],
                            })
    except Exception:
        pass
    return findings


def scope_docker(package, version, php_version):
    """Scan a specific package in a Docker container."""
    scanner_script = r'''
echo "=== SCAN RESULTS ==="
find /var/www/html/vendor -name "*.php" -not -path "*/tests/*" 2>/dev/null | while read f; do
  has_input=$(grep -l "\$_GET\|\$_POST\|\$_REQUEST\|\$_COOKIE\|php://input" "$f" 2>/dev/null)
  if [ -n "$has_input" ]; then
    echo "INPUT: $f"
    grep -n "\$_GET\|\$_POST\|\$_REQUEST\|\$_COOKIE\|php://input\|file_put_contents\|eval\|system\|exec\|unserialize" "$f" 2>/dev/null | head -10
    echo ""
  fi
done
echo "=== DONE ==="
'''
    pkgname = package.replace("/", "_")
    tag = f"scan-{pkgname}"
    subprocess.run(["docker", "rm", "-f", tag], capture_output=True, check=False)  # skipcq: BAN-B607

    base_tag = f"wargame-dist-challenge-base-php{php_version.replace('.', '')}"
    r = subprocess.run([  # skipcq: BAN-B607
        "docker", "build", "--quiet", "--file", "dist/challenge/Dockerfile",
        "--build-arg", f"CHALLENGE_BASE={base_tag}:latest",
        "--build-arg", f"PACKAGE_NAME={package}",
        "--build-arg", f"PACKAGE_VERSION={version}",
        "--build-arg", "FLAG1=TF1", "--build-arg", "FLAG2=TF2",
        "-t", tag, "dist/challenge/"
    ], capture_output=True, text=True, timeout=120, check=False)

    if r.returncode != 0:
        print(f"[-] BUILD FAILED: {r.stderr[-200:]}")
        return

    result = subprocess.run(  # skipcq: BAN-B607
        ["docker", "exec", tag, "sh", "-c", scanner_script],
        capture_output=True, text=True, timeout=30, check=False
    )
    print(result.stdout)
    subprocess.run(["docker", "rm", "-f", tag], capture_output=True, check=False)  # skipcq: BAN-B607


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Unified vulnerability scanner")
    parser.add_argument(
        "--scope", required=True,
        choices=["local", "deep", "global", "docker", "targeted"],
        help="Scan scope (local, deep, global, docker, targeted)"
    )
    parser.add_argument("args", nargs="*", help="Additional arguments (packages for local/targeted, or pkg ver php for docker)")
    args = parser.parse_args()

    if args.scope in ("local", "targeted"):
        scope_local(filter_names=args.args if args.args else None)
    elif args.scope == "deep":
        scope_deep()
    elif args.scope == "global":
        scope_global()
    elif args.scope == "docker":
        if len(args.args) < 3:
            print("Usage: scan.py --scope docker PACKAGE VERSION PHP_VERSION")
            sys.exit(1)
        scope_docker(args.args[0], args.args[1], args.args[2])
    else:
        print(f"[-] Scope '{args.scope}' not recognized")


if __name__ == "__main__":
    main()
