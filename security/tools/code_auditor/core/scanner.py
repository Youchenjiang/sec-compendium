"""
Unified PHP Vulnerability Scanner
Combines basic scanning, advanced scanning, and deep data-flow analysis.
Single source of truth for all scanning functionality.
"""
import os
import re
from pathlib import Path

from .scanner_rules import CORE_RULES, BROAD_RULES, ALL_RULES
from .types import Vulnerability
from .scanner_utils import (
    read_php_file, strip_comments, has_superglobal,
    SUPERGLOBALS,
)

HINTS = {
    "code_execution": "Inject PHP code via parameter",
    "command_injection": "Inject OS command via parameter",
    "file_operation": "Exploit file write/read via user input",
    "file_inclusion": "Use path traversal to include arbitrary files",
    "deserialization": "Craft malicious serialized object",
    "sql_injection": "Use UNION SELECT or time-based blind injection",
    "path_traversal": "Use ../ to access arbitrary files",
    "type_juggling": "Exploit type coercion in loose comparison",
    "auth_bypass": "Bypass authentication check",
    "object_injection": "Exploit magic methods via unserialize",
    "weak_crypto": "Exploit weak cryptographic primitives",
    "info_disclosure": "Extract sensitive info from debug output",
    "ssrf": "Redirect requests to internal services",
}


class Scanner:
    """Unified scanner combining basic, advanced, and deep analysis."""

    def __init__(self, tier=None, deep=False):
        if tier == "CORE":
            self.rules = CORE_RULES
        elif tier == "BROAD":
            self.rules = BROAD_RULES
        else:
            self.rules = list(ALL_RULES)
        self.deep = deep
        self.findings = []
        self.scanned_files = 0

    def scan_directory(self, directory, extensions=None):
        if extensions is None:
            extensions = ['.php']
        self.findings = []
        self.scanned_files = 0
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ("vendor", ".git", "node_modules")]
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    self.scan_file(file_path)
        return self.findings

    def scan_file(self, file_path):
        content = read_php_file(file_path)
        if content is None:
            return []

        self.scanned_files += 1
        file_findings = []
        lines = content.split("\n")

        # Single-line pattern matching
        in_block = False
        for line_num, line in enumerate(lines, 1):
            stripped, in_block = strip_comments(line, in_block)
            if not stripped:
                continue
            for rule in self.rules:
                if rule.search(stripped):
                    finding = Vulnerability(
                        rule_id=rule.id,
                        vuln_type=rule.name,
                        severity=rule.severity,
                        category=rule.category,
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=stripped[:120],
                        description=rule.description or rule.name,
                        exploit_hint=HINTS.get(rule.category, "Analyze the vulnerability"),
                    )
                    file_findings.append(finding)
                    self.findings.append(finding)

        # Deep scan: multi-line data-flow analysis
        if self.deep:
            file_findings.extend(self._deep_analysis(content, file_path, lines))

        return file_findings

    def _deep_analysis(self, content, file_path, lines):
        """Multi-line data-flow analysis: $_INPUT -> dangerous sink."""
        deep_findings = []

        # Check $_INPUT -> file_put_contents
        if has_superglobal(content) and "file_put_contents" in content:
            matches = re.finditer(
                r'(\$\w+\s*=[^;]*\$_(?:GET|POST|REQUEST)[\s\S]{1,500}?file_put_contents\s*\([^;]+\))',
                content,
            )
            for m in matches:
                line_no = content[:m.start()].count("\n") + 1
                deep_findings.append(Vulnerability(
                    rule_id="DEEP-TAINT-WRITE",
                    vuln_type="Multi-line File Write / Code Injection",
                    severity="HIGH",
                    category="file_operation",
                    file_path=file_path,
                    line_number=line_no,
                    code_snippet=m.group(1).replace("\n", " ")[:140],
                    description="User input assigned to variable and written via file_put_contents",
                    exploit_hint="Tainted file write -- inject PHP code",
                ))

        # Standalone entry point detection
        if has_superglobal(content):
            lower_name = Path(file_path).name.lower()
            if any(k in lower_name for k in ["install", "setup", "config", "upload"]):
                for idx, line in enumerate(lines, 1):
                    if SUPERGLOBALS.search(line):
                        deep_findings.append(Vulnerability(
                            rule_id="DEEP-ENTRY",
                            vuln_type="Standalone Entry Point with User Input",
                            severity="MEDIUM",
                            category="file_inclusion",
                            file_path=file_path,
                            line_number=idx,
                            code_snippet=f"Standalone {Path(file_path).name} taking user inputs directly",
                            description="Web-accessible PHP processing direct HTTP requests",
                            exploit_hint="Direct entry point -- test for all input vectors",
                        ))
                        break

        self.findings.extend(deep_findings)
        return deep_findings

    def get_summary(self):
        by_severity = {}
        by_category = {}
        for f in self.findings:
            sev = f["severity"]
            cat = f["category"]
            by_severity[sev] = by_severity.get(sev, 0) + 1
            by_category[cat] = by_category.get(cat, 0) + 1
        return {
            "total": len(self.findings),
            "by_severity": by_severity,
            "by_category": by_category,
            "files_scanned": self.scanned_files,
        }


# Convenience functions
def scan_package(package_dir, deep=False):
    """Scan a single package directory."""
    scanner = Scanner(deep=deep)
    findings = scanner.scan_directory(package_dir)
    return findings, scanner.get_summary()


def scan_directory(directory, tier=None, deep=False):
    """Scan any directory."""
    scanner = Scanner(tier=tier, deep=deep)
    findings = scanner.scan_directory(directory)
    return findings, scanner.get_summary()


def scan_file(file_path, tier=None, deep=False):
    """Scan a single file."""
    scanner = Scanner(tier=tier, deep=deep)
    findings = scanner.scan_file(file_path)
    return findings, scanner.get_summary()
