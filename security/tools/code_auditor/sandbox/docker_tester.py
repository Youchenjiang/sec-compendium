"""
Code Auditor - Docker Sandbox Tester
Tests exploits against local challenge containers.
"""
import os
import shutil
import subprocess
import time
from typing import Dict, Tuple
from pathlib import Path

BASH_BIN = shutil.which("bash") or "bash"


class DockerTester:
    """Tests exploits using Docker containers."""

    def __init__(self, dist_dir: str):
        self.dist_dir = Path(dist_dir)
        self.containers_running = False

    def setup_environment(self) -> bool:
        """Setup Docker environment (build base images if needed)."""
        print("[*] Setting up Docker environment...")

        # Check if dist directory exists
        if not self.dist_dir.exists():
            print(f"[-] Dist directory not found: {self.dist_dir}")
            return False

        # Build base images
        build_script = self.dist_dir / "build-base-images.sh"
        if build_script.exists():
            print("[*] Building base images (if needed)...")
            result = subprocess.run(
                [BASH_BIN, str(build_script)],
                cwd=str(self.dist_dir),
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes max
                check=False,
            )
            if result.returncode != 0:
                print(f"[-] Build failed: {result.stderr}")
                return False
            print("[+] Base images built successfully")

        return True

    def test_exploit(
        self,
        exploit_path: str,
        php_version: str,
        package_name: str,
        package_version: str,
        timeout: int = 120,
        storage=None
    ) -> Tuple[bool, str, str]:
        """
        Test an exploit against a local challenge container.
        Returns: (success, output)
        """
        run_script = self.dist_dir / "run.sh"
        if not run_script.exists():
            return False, "run.sh not found in dist directory", "- Missing run.sh in dist directory"

        # Make exploit executable
        os.chmod(exploit_path, 0o700)  # skipcq: PTC-W6004

        print(f"[*] Testing exploit: {exploit_path}")
        print(f"[*] Package: {package_name}:{package_version} (PHP {php_version})")

        analysis = ""

        try:
            # Start containers and run exploit
            result = subprocess.run(
                [
                    BASH_BIN, str(run_script),
                    php_version,
                    package_name,
                    package_version,
                    exploit_path
                ],
                cwd=str(self.dist_dir),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            output = result.stdout + result.stderr

            # Check for flags or command execution in output
            output_lower = output.lower()
            has_flag = any(k in output_lower for k in ["flag", "hitcon", "ctf{", "flag{", "local_test"]) or "root:" in output or "uid=0" in output
            has_flag1 = "LOCAL_TEST_FLAG1" in output or "flag1" in output_lower or "hitcon" in output_lower
            has_flag2 = "LOCAL_TEST_FLAG2" in output or "flag2" in output_lower

            if has_flag or has_flag1 or has_flag2:
                print("[+] Exploit successful!")
                print(f"    Flag 1: {'Found' if has_flag1 else 'Not found'}")
                print(f"    Flag 2: {'Found' if has_flag2 else 'Not found'}")
                # Save success log
                if storage:
                    storage.save_test_log(package_name, exploit_path, output, True)
                return True, output, ""
            else:
                print("[-] Exploit did not capture flags")
                # Auto-analyze failure
                if storage:
                    analysis = storage.save_failure_analysis(package_name, exploit_path, output)
                    storage.save_test_log(package_name, exploit_path, output, False, analysis)
                    print("    Diagnosis:")
                    for line in analysis.split("\n"):
                        print(f"      {line}")
                return False, output, analysis

        except subprocess.TimeoutExpired:
            print(f"[-] Test timed out after {timeout} seconds")
            output = "TIMEOUT: Container did not respond within timeout"
            analysis = "- Timeout: 靶機可能沒啟動，或 exploit 卡在 HTTP request"
            if storage:
                storage.save_test_log(package_name, exploit_path, output, False, analysis)
            self.cleanup()
            return False, output, analysis
        except Exception as e:
            print(f"[-] Error during test: {e}")
            output = str(e)
            analysis = f"- Exception: {e}"
            if storage:
                storage.save_test_log(package_name, exploit_path, output, False, analysis)
            return False, output, analysis

    def cleanup(self):
        """Stop and remove containers."""
        if self.dist_dir.exists():
            run_script = self.dist_dir / "run.sh"
            if run_script.exists():
                print("[*] Cleaning up containers...")
                subprocess.run(
                    [BASH_BIN, str(run_script), "down"],
                    cwd=str(self.dist_dir),
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.containers_running = False

    def test_all_php_versions(
        self,
        exploit_path: str,
        package_name: str,
        package_version: str
    ) -> Dict[str, bool]:
        """Test exploit against multiple PHP versions."""
        results = {}
        php_versions = ["7.4.33", "8.4"]

        for php_version in php_versions:
            print(f"\n[*] Testing with PHP {php_version}...")
            success, _, _ = self.test_exploit(
                exploit_path,
                php_version,
                package_name,
                package_version
            )
            results[php_version] = success
            self.cleanup()
            time.sleep(2)  # Brief pause between tests

        return results


def create_tester(dist_dir: str) -> DockerTester:
    """Create and return a Docker tester instance."""
    return DockerTester(dist_dir)
