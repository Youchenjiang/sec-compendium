#!/usr/bin/env python3
"""
HITCON 2026 Wargame Bot - Main Orchestrator
Automates vulnerability scanning, exploit generation, testing, and submission.
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add current directory and project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from client import create_client
from lib.scanner import Scanner
from lib.types import Vulnerability
from generator import create_generator
from tester import create_tester
from storage import Storage, RunRecord
import config


class WargameBot:
    """Main orchestrator for automated exploit development."""

    def __init__(self, dist_dir: str = None, email: str = None, password: str = None):
        self.dist_dir = dist_dir or config.DIST_DIR
        self.client = create_client(email, password)
        self.scanner = Scanner()
        self.generator = create_generator()
        self.tester = create_tester(self.dist_dir) if self.dist_dir else None

        # Storage
        self.storage = Storage()

        # Results tracking
        self.results = {
            "packages_scanned": 0,
            "vulnerabilities_found": 0,
            "exploits_generated": 0,
            "exploits_tested": 0,
            "exploits_submitted": 0,
            "successful_submissions": []
        }

    @staticmethod
    def _resolve_offline_package(local_dir: str, target_package: str = None) -> Optional[List[Dict[str, Any]]]:
        """Resolve package metadata from local directory."""
        if not local_dir:
            print("[-] Offline mode specified without --local-dir or target source. Exiting.")
            return None
        p = Path(local_dir).resolve()
        if not p.exists():
            print(f"[-] Specified local directory does not exist: {p}")
            return None
        pkg_name = target_package or p.name
        composer_json = p / "composer.json"
        if composer_json.exists():
            try:
                cdata = json.loads(composer_json.read_text(encoding="utf-8"))
                pkg_name = cdata.get("name", pkg_name)
            except Exception:
                pass
        return [{
            "id": "local",
            "name": pkg_name,
            "version": "local",
            "php_version": "8.4",
            "source_path": str(p),
        }]

    def _fetch_online_packages(self, target_package: str = None) -> Optional[List[Dict[str, Any]]]:
        """Authenticate and fetch online packages."""
        print("\n[Phase 1] Authentication")
        if not self.client.login():
            print("[-] Failed to authenticate. Exiting.")
            return None

        print("\n[Phase 2] Fetching packages")
        packages = self.client.get_packages()
        if not packages:
            print("[-] No packages found. Exiting.")
            return None

        if target_package:
            packages = [p for p in packages if target_package in p.get("name", "")]
            if not packages:
                print(f"[-] Package '{target_package}' not found. Exiting.")
                return None
        return packages

    def run(
        self,
        target_package: str = None,
        scan_only: bool = False,
        local_dir: str = None,
        no_submit: bool = False,
        offline: bool = False,
    ):
        """Main execution flow."""  # skipcq: PYL-R0912
        print("=" * 60)
        print("HITCON 2026 Wargame Bot")
        print("=" * 60)

        is_offline = offline or bool(local_dir)
        if is_offline:
            print("\n[Phase 1] Offline Mode (skipping platform login)")
            packages = self._resolve_offline_package(local_dir, target_package)
        else:
            packages = self._fetch_online_packages(target_package)

        if not packages:
            return

        print(f"[*] Processing {len(packages)} packages")

        # Step 3: Process each package
        for i, package in enumerate(packages, 1):
            print(f"\n{'=' * 60}")
            print(f"[{i}/{len(packages)}] Processing: {package.get('name')}:{package.get('version')}")
            print(f"    PHP Version: {package.get('php_version')}")
            print(f"    Stars: {package.get('stars', 'N/A')}")
            print(f"    Downloads: {package.get('downloads', 'N/A')}")
            print("=" * 60)

            self.process_package(
                package,
                scan_only=scan_only,
                no_submit=no_submit or is_offline,
            )

            # Respect submission cooldown if multiple online packages
            if i < len(packages) and not is_offline:
                print(f"\n[*] Waiting {config.SUBMISSION_COOLDOWN}s before next package...")
                time.sleep(config.SUBMISSION_COOLDOWN)

        # Step 4: Summary
        self.print_summary()

        # Step 5: Print storage location
        print(f"\n[+] All results saved to: {self.storage.base_dir}")
        stats = self.storage.get_stats()
        print(f"    Total packages processed: {stats['total_runs']}")
        print(f"    Total submissions: {stats['total_submissions']}")

    def process_package(
        self,
        package: Dict[str, Any],
        scan_only: bool = False,
        no_submit: bool = False,
    ):
        """Process a single package."""
        package_name = package.get("name")
        package_version = package.get("version")
        php_version = package.get("php_version")
        source_path = package.get("source_path")

        # Track everything for this package
        exploit_results = {}

        # Step 3.1: Download and scan package
        print("\n[Phase 3] Scanning for vulnerabilities")
        vulnerabilities = self.scan_package(package_name, package_version, source_override=source_path)
        self.results["packages_scanned"] += 1

        # Save vulnerability report
        if vulnerabilities:
            self.storage.save_vulnerability_report(package_name, vulnerabilities)

        if not vulnerabilities:
            print("[!] No vulnerabilities found. Skipping.")
            return

        if scan_only:
            print("[*] --scan-only requested. Skipping exploit generation, testing, and submission.")
            return

        # Step 3.2: Generate exploits
        print("\n[Phase 4] Generating exploits")
        exploits = self.generate_exploits(vulnerabilities, package)

        # Step 3.3: Test exploits (if Docker is available)
        if self.tester:
            print("\n[Phase 5] Testing exploits")
            working_exploits = self.test_exploits(exploits, package, exploit_results=exploit_results)
        else:
            print("\n[!] Docker tester not available. Skipping testing.")
            working_exploits = exploits  # Assume all work

        # Step 3.4: Submit working exploits
        submission_result = None
        if working_exploits:
            if no_submit:
                print("\n[Phase 6] Submissions skipped (--no-submit or offline mode).")
                submission_result = {"status": "skipped", "reason": "offline_or_no_submit"}
            else:
                print("\n[Phase 6] Submitting exploits")
                submission_result = self.submit_exploits(working_exploits, package)

        # Step 3.5: Generate writeup for this package
        record = RunRecord(
            timestamp=datetime.now().isoformat(),
            package_name=package_name,
            package_version=package_version,
            php_version=php_version,
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
            exploits_generated=[str(e) for e in exploits],
            exploit_results=exploit_results,
            submission_result=submission_result,
        )
        self.storage.record_run(record)
        self.storage.generate_writeup(record)

    def scan_package(
        self,
        package_name: str,
        package_version: str,
        source_override: str = None,
    ) -> List[Vulnerability]:
        """Download and scan a package for vulnerabilities."""
        print(f"[*] Locating/downloading {package_name}:{package_version}...")

        # If explicit source override provided (e.g. from --local-dir)
        if source_override and Path(source_override).exists():
            override_path = Path(source_override).resolve()
            print(f"[*] Using explicit source at: {override_path}")
            if override_path.is_file():
                vulnerabilities = self.scanner.scan_file(str(override_path))
            else:
                vulnerabilities = self.scanner.scan_directory(str(override_path))
            self.results["vulnerabilities_found"] += len(vulnerabilities)
            return vulnerabilities

        # Try multiple locations for package source code
        parent_dir = Path(__file__).parent.parent
        pkg_short = package_name.split("/")[-1] if "/" in package_name else package_name

        search_paths = []
        if self.dist_dir:
            dist = Path(self.dist_dir)
            search_paths.extend([
                dist / "challenge" / "vendor" / package_name,
                dist / "vendor" / package_name,
                dist / package_name,
                dist / pkg_short,
                dist / "challenge" / "vendor",
                dist / "vendor",
                dist,
            ])

        # Also search in workspace parent directories
        search_paths.extend([
            parent_dir / "rbac-2.0.0" / "PhpRbac" / "src",
            parent_dir / "rbac-2.0.0" / "PhpRbac",
            parent_dir / pkg_short,
            parent_dir / "packages" / pkg_short,
        ])

        for vendor_path in search_paths:
            if vendor_path and vendor_path.exists():
                print(f"[*] Found source at: {vendor_path}")
                if vendor_path.is_file():
                    vulnerabilities = self.scanner.scan_file(str(vendor_path))
                else:
                    vulnerabilities = self.scanner.scan_directory(str(vendor_path))
                self.results["vulnerabilities_found"] += len(vulnerabilities)
                return vulnerabilities

        # Also scan install.php specifically if present
        install_php = parent_dir / "rbac-2.0.0" / "PhpRbac" / "install.php"
        if install_php.exists():
            print(f"[*] Found install.php at: {install_php}")
            vulnerabilities = self.scanner.scan_file(str(install_php))
            self.results["vulnerabilities_found"] += len(vulnerabilities)
            return vulnerabilities

        print("[!] Could not locate package files for scanning")
        return []

    def generate_exploits(self, vulnerabilities: List[Vulnerability], package: Dict[str, Any]) -> List[str]:
        """Generate exploit scripts for found vulnerabilities."""
        exploits = []

        # Sort by severity (high first)
        vulnerabilities.sort(key=lambda v: 0 if v.severity == "high" else 1)

        for vuln in vulnerabilities[:5]:  # Limit to top 5 vulnerabilities
            print(f"\n[*] Generating exploit for: {vuln.vuln_type}")
            print(f"    File: {vuln.file_path}:{vuln.line_number}")
            print(f"    Code: {vuln.code_snippet}")

            exploit_code = self.generator.generate_exploit(vuln, package)
            if exploit_code:
                # Save exploit to persistent storage
                vuln_type = vuln.vuln_type.lower().replace(" ", "_")
                exploit_path = self.storage.save_exploit(
                    package.get("name"),
                    vuln_type,
                    exploit_code
                )
                exploits.append(str(exploit_path))
                self.results["exploits_generated"] += 1

        return exploits

    def test_exploits(
        self,
        exploits: List[str],
        package: Dict[str, Any],
        exploit_results: Dict[str, Any] = None,
    ) -> List[str]:
        """Test exploits against local challenge containers."""
        if exploit_results is None:
            exploit_results = {}
        working_exploits = []
        package_name = package.get("name")
        package_version = package.get("version")
        php_version = package.get("php_version")

        for exploit_path in exploits:
            print(f"\n[*] Testing: {exploit_path}")

            success, output, analysis = self.tester.test_exploit(
                exploit_path,
                php_version,
                package_name,
                package_version,
                storage=self.storage
            )

            self.results["exploits_tested"] += 1

            # Track result for writeup
            exploit_results[exploit_path] = {
                "success": success,
                "output": output[:500] if output else "",
                "analysis": analysis,
            }

            if success:
                working_exploits.append(exploit_path)
                print(f"[+] Exploit works: {exploit_path}")
            else:
                print(f"[-] Exploit failed: {exploit_path}")
                if analysis:
                    print("    Diagnosis:")
                    for line in analysis.split("\n"):
                        print(f"      {line}")

            # Clean up
            self.tester.cleanup()
            time.sleep(2)

        return working_exploits

    def submit_exploits(self, exploits: List[str], package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Submit working exploits to the wargame platform."""
        package_id = package.get("id")
        last_result = None

        for exploit_path in exploits:
            print(f"\n[*] Submitting: {exploit_path}")

            try:
                with open(exploit_path, 'r', encoding='utf-8') as f:
                    exploit_content = f.read()

                result = self.client.submit_exploit(package_id, exploit_content)
                last_result = result

                if "error" not in result:
                    self.results["exploits_submitted"] += 1
                    self.results["successful_submissions"].append({
                        "package": package.get("name"),
                        "exploit": exploit_path,
                        "result": result
                    })
                    print("[+] Submitted successfully")
                else:
                    print(f"[-] Submission failed: {result['error']}")

            except Exception as e:
                print(f"[-] Error reading exploit: {e}")

        return last_result

    def print_summary(self):
        """Print execution summary."""
        print("\n" + "=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Packages scanned:      {self.results['packages_scanned']}")
        print(f"Vulnerabilities found: {self.results['vulnerabilities_found']}")
        print(f"Exploits generated:    {self.results['exploits_generated']}")
        print(f"Exploits tested:       {self.results['exploits_tested']}")
        print(f"Exploits submitted:    {self.results['exploits_submitted']}")
        print(f"Successful submissions: {len(self.results['successful_submissions'])}")

        if self.results['successful_submissions']:
            print("\nSuccessful submissions:")
            for sub in self.results['successful_submissions']:
                print(f"  - {sub['package']}: {sub['exploit']}")

        print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="HITCON 2026 Wargame Bot")
    parser.add_argument("--email", help="Wargame account email")
    parser.add_argument("--password", help="Wargame account password")
    parser.add_argument("--dist-dir", help="Path to dist directory")
    parser.add_argument("--local-dir", help="Path to local package or project source to analyze")
    parser.add_argument("--package", help="Target specific package")
    parser.add_argument("--scan-only", action="store_true", help="Only scan, don't generate exploits")
    parser.add_argument("--offline", action="store_true", help="Run offline without connecting/logging in to platform")
    parser.add_argument("--no-submit", action="store_true", help="Generate and test exploits without submitting to platform")
    parser.add_argument("--no-docker", action="store_true", help="Skip Docker testing")

    args = parser.parse_args()

    # Create bot instance
    bot = WargameBot(
        dist_dir=args.dist_dir,
        email=args.email,
        password=args.password
    )

    # Disable Docker testing if requested
    if args.no_docker:
        bot.tester = None

    # Run bot
    bot.run(
        target_package=args.package,
        scan_only=args.scan_only,
        local_dir=args.local_dir,
        no_submit=args.no_submit,
        offline=args.offline,
    )


if __name__ == "__main__":
    main()
