"""
Code Auditor - Core Engine Class
Unified orchestrator for white-box static analysis, PoC generation, sandbox verification, and reporting.
"""
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .core.scanner import Scanner
from .core.types import Vulnerability
from .generator.exploit_gen import create_generator
from .sandbox.docker_tester import create_tester
from .storage.recorder import Storage, RunRecord
from .platform.base import BasePlatformClient
from .platform.local import LocalDirectoryClient
from . import config


# Safe stdout UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class CodeAuditor:
    """Unified engine for white-box code audit, exploit generation, and dynamic verification."""

    def __init__(
        self,
        platform_client: Optional[BasePlatformClient] = None,
        dist_dir: Optional[str] = None,
        enable_sandbox: bool = False,
        storage: Optional[Storage] = None,
    ):
        self.client = platform_client
        self.dist_dir = dist_dir or config.DIST_DIR
        self.scanner = Scanner(deep=True)
        self.generator = create_generator()
        self.storage = storage or Storage()
        self.tester = create_tester(self.dist_dir) if (enable_sandbox and self.dist_dir) else None

        self.stats = {
            "targets_scanned": 0,
            "vulnerabilities_found": 0,
            "exploits_generated": 0,
            "exploits_tested": 0,
            "submissions_completed": 0,
        }

    def audit_directory(self, target_dir: str, scan_only: bool = True, verify: bool = False):
        """Perform full audit of a local directory or package."""
        p = Path(target_dir).resolve()
        if not p.exists():
            print(f"[-] Target directory not found: {p}")
            return

        client = LocalDirectoryClient(target_dir=str(p))
        self.client = client
        self.run(scan_only=scan_only, verify=verify)

    def run(
        self,
        target_name: Optional[str] = None,
        scan_only: bool = False,
        verify: bool = False,
        no_submit: bool = False,
    ):
        """Execute the audit workflow."""
        print("=" * 65)
        print(" [Code Auditor] Automated White-Box Security Audit Engine")
        print("=" * 65)

        if not self.client:
            print("[-] No platform or local client configured. Exiting.")
            return

        # 1. Platform Authentication
        print("\n[Phase 1] Platform / Target Setup")
        if not self.client.login():
            print("[-] Authentication failed. Exiting.")
            return
        print("[+] Ready.")

        # 2. Target Discovery
        print("\n[Phase 2] Discovering Targets")
        targets = self.client.get_targets()
        if not targets:
            print("[-] No targets found to audit.")
            return

        if target_name:
            targets = [t for t in targets if target_name in t.get("name", "")]
            if not targets:
                print(f"[-] Target '{target_name}' not found.")
                return

        print(f"[*] Analyzing {len(targets)} target(s)...")

        # 3. Process Each Target
        for i, target in enumerate(targets, 1):
            pkg_name = target.get("name", f"target_{i}")
            pkg_ver = target.get("version", "local")
            php_ver = target.get("php_version", "8.4")

            print(f"\n{'=' * 65}")
            print(f"[{i}/{len(targets)}] Auditing: {pkg_name} ({pkg_ver}) [PHP {php_ver}]")
            print(f"{'=' * 65}")

            self._process_target(
                target,
                scan_only=scan_only,
                verify=verify,
                no_submit=no_submit or isinstance(self.client, LocalDirectoryClient),
            )

        # 4. Summary & Report Storage
        self._print_summary()

    def _process_target(
        self,
        target: Dict[str, Any],
        scan_only: bool = False,
        verify: bool = False,
        no_submit: bool = False,
    ):
        pkg_name = target.get("name")
        pkg_ver = target.get("version")
        php_ver = target.get("php_version", "8.4")
        source_override = target.get("source_path")

        # Step 3.1: Scan Source
        print("\n[Phase 3] Static Analysis & AST Taint Tracking")
        vulnerabilities = self._scan_source(pkg_name, pkg_ver, source_override)
        self.stats["targets_scanned"] += 1

        if vulnerabilities:
            self.storage.save_vulnerability_report(pkg_name, vulnerabilities)

        if not vulnerabilities:
            print("[+] No vulnerabilities detected in this target.")
            return

        if scan_only:
            print("[*] Scan-only completed. Skipping exploit generation and verification.")
            return

        # Step 3.2: PoC / Exploit Generation
        print("\n[Phase 4] Automated PoC / Exploit Synthesis")
        exploits = []
        for vuln in vulnerabilities[:5]:
            code = self.generator.generate_exploit(vuln, target)
            if code:
                vtype = vuln.vuln_type.lower().replace(" ", "_").replace("/", "_")
                saved = self.storage.save_exploit(pkg_name, vtype, code)
                exploits.append(str(saved))
                self.stats["exploits_generated"] += 1

        # Step 3.3: Dynamic Verification (Docker)
        working_exploits = []
        exploit_results = {}
        if verify and self.tester:
            print("\n[Phase 5] Docker Sandbox Dynamic Verification")
            for exp in exploits:
                self.stats["exploits_tested"] += 1
                success, _, analysis = self.tester.test_exploit(
                    exp, php_ver, pkg_name, pkg_ver, storage=self.storage
                )
                exploit_results[exp] = {"success": success, "analysis": analysis}
                if success:
                    working_exploits.append(exp)
        elif verify and not self.tester:
            print("[-] Dynamic verification was requested (--verify), but no docker tester is available (dist_dir not configured). Skipping submission.")
            working_exploits = []
        else:
            working_exploits = exploits

        # Step 3.4: Submission or Output
        submission_result = None
        if working_exploits and not no_submit:
            print("\n[Phase 6] Submitting Validated Exploit to Platform")
            target_id = target.get("id", pkg_name)
            for exp in working_exploits:
                try:
                    with open(exp, "r", encoding="utf-8") as f:
                        payload = f.read()
                    submission_result = self.client.submit(target_id, payload)
                    self.stats["submissions_completed"] += 1
                except Exception as e:
                    print(f"[-] Submission failed: {e}")

        # Step 3.5: Generate Report / Writeup
        record = RunRecord(
            timestamp=datetime.now().isoformat(),
            package_name=pkg_name,
            package_version=pkg_ver,
            php_version=php_ver,
            vulnerabilities=[
                {
                    "type": v.vuln_type,
                    "file": v.file_path,
                    "line": v.line_number,
                    "code": v.code_snippet,
                    "severity": v.severity,
                    "description": v.description,
                    "exploit_hint": v.exploit_hint,
                }
                for v in vulnerabilities
            ],
            exploits_generated=exploits,
            exploit_results=exploit_results,
            submission_result=submission_result,
        )
        self.storage.record_run(record)
        self.storage.generate_writeup(record)

    def _scan_source(self, name: str, version: str, source_override: Optional[str]) -> List[Vulnerability]:
        if source_override and Path(source_override).exists():
            override_path = Path(source_override).resolve()
            if override_path.is_file():
                findings = self.scanner.scan_file(str(override_path))
            else:
                findings = self.scanner.scan_directory(str(override_path))
            self.stats["vulnerabilities_found"] += len(findings)
            return findings

        # Dynamic search in dist_dir or search paths
        if self.dist_dir:
            dist = Path(self.dist_dir)
            candidates = [
                dist / "challenge" / "vendor" / name,
                dist / "vendor" / name,
                dist / name,
                dist / name.split("/")[-1],
                dist,
            ]
            for c in candidates:
                if c.exists():
                    findings = self.scanner.scan_directory(str(c))
                    self.stats["vulnerabilities_found"] += len(findings)
                    return findings

        print(f"[!] Unable to locate source code files for target: {name}")
        return []

    def _print_summary(self):
        print("\n" + "=" * 65)
        print(" AUDIT EXECUTION SUMMARY")
        print("=" * 65)
        print(f" Targets Scanned:         {self.stats['targets_scanned']}")
        print(f" Vulnerabilities Found:   {self.stats['vulnerabilities_found']}")
        print(f" Exploits Generated:      {self.stats['exploits_generated']}")
        print(f" Exploits Tested:         {self.stats['exploits_tested']}")
        print(f" Submissions Completed:   {self.stats['submissions_completed']}")
        print(f" Results & Writeups:      {self.storage.base_dir}")
        print("=" * 65)
