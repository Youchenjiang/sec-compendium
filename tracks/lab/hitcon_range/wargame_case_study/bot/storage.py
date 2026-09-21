"""
HITCON 2026 Wargame Bot - Storage & Writeup Generator
Persists all exploits, logs, findings, and auto-generates writeups.
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add project root to path for shared lib
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.paths import RESULTS_DIR
from lib.types import Vulnerability


@dataclass
class RunRecord:
    """Record of a single bot run."""
    timestamp: str
    package_name: str
    package_version: str
    php_version: str
    vulnerabilities: List[Dict[str, Any]]
    exploits_generated: List[str]
    exploit_results: Dict[str, Any]  # exploit_path -> {success, output, submitted}
    submission_result: Optional[Dict[str, Any]]


class Storage:
    """Persistent storage for all bot artifacts."""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = str(RESULTS_DIR)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Sub-directories
        self.exploits_dir = self.base_dir / "exploits"
        self.logs_dir = self.base_dir / "logs"
        self.reports_dir = self.base_dir / "reports"
        self.writeups_dir = self.base_dir / "writeups"

        for d in [self.exploits_dir, self.logs_dir, self.reports_dir, self.writeups_dir]:
            d.mkdir(exist_ok=True)

        # Run history
        self.history_file = self.base_dir / "history.jsonl"

    def save_exploit(self, package_name: str, vuln_type: str, exploit_code: str) -> Path:
        """Save exploit script with metadata."""
        safe_name = package_name.replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{vuln_type}_{timestamp}.py"

        package_dir = self.exploits_dir / safe_name
        package_dir.mkdir(exist_ok=True)

        exploit_path = package_dir / filename
        exploit_path.write_text(exploit_code, encoding="utf-8")

        print(f"[+] Exploit saved: {exploit_path}")
        return exploit_path

    def save_test_log(self, package_name: str, exploit_path: str, output: str, success: bool, analysis: str = None):
        """Save test execution log with optional failure analysis."""
        safe_name = package_name.replace("/", "_")
        log_dir = self.logs_dir / safe_name
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "SUCCESS" if success else "FAILED"
        log_file = log_dir / f"{status}_{timestamp}.log"

        log_content = f"""=== Test Log ===
Timestamp: {datetime.now().isoformat()}
Package: {package_name}
Exploit: {exploit_path}
Status: {status}

=== Output ===
{output}
"""
        if analysis:
            log_content += f"""
=== Failure Analysis ===
{analysis}
"""

        log_file.write_text(log_content, encoding="utf-8")
        print(f"[+] Log saved: {log_file}")

    def save_vulnerability_report(self, package_name: str, vulnerabilities: List[Vulnerability]):
        """Save vulnerability scan report as JSON."""
        safe_name = package_name.replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report = {
            "package": package_name,
            "timestamp": datetime.now().isoformat(),
            "total_vulnerabilities": len(vulnerabilities),
            "vulnerabilities": [
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
            ]
        }

        report_file = self.reports_dir / f"{safe_name}_{timestamp}.json"
        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[+] Report saved: {report_file}")
        return report_file

    @staticmethod
    def save_failure_analysis(package_name: str, exploit_path: str, output: str) -> str:
        """Analyze failure output and return a diagnosis string."""
        analysis_lines = []
        output_lower = output.lower()

        rules = [
            (('timeout', 'timed out'), "- Timeout: 靶機可能沒啟動或連線失敗"),
            (('connection refused', 'connectionreset'), "- Connection refused: Apache 沒跑或 port 不對"),
            (('404', 'not found'), "- 404 Not Found: URL 路徑不對，確認 install.php 是否可存取"),
            (('permission denied',), "- Permission denied: 檔案權限不足"),
            (('syntax error', 'parse error'), "- PHP syntax error: payload 格式有問題"),
            (('call to undefined function',), "- Function not found: PHP 版本不支援該函數"),
            (('stack trace', 'fatal error'), "- PHP error occurred, 但 exploit 可能已部分執行"),
        ]
        for keywords, msg in rules:
            if any(k in output_lower for k in keywords):
                analysis_lines.append(msg)

        if not any(k in output_lower for k in ('flag', 'hitcon', 'local_test')):
            analysis_lines.append("- No flag in output: exploit payload 沒有觸發 RCE")
            analysis_lines.append("  可能原因: install.php 不存在、process 參數不對、或 payload 格式錯誤")

        if not analysis_lines:
            analysis_lines.append("- 無法自動診斷，需人工檢查 output")

        return "\n".join(analysis_lines)

    def record_run(self, record: RunRecord):
        """Append a run record to history."""
        entry = asdict(record)
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_history(self) -> List[RunRecord]:
        """Load all run history."""
        records = []
        if self.history_file.exists():
            for line in self.history_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    records.append(RunRecord(**json.loads(line)))
        return records

    @staticmethod
    def _format_vuln_rows(vulnerabilities: list) -> str:
        return "".join(
            f"| {i} | {v['type']} | {v['severity']} | `{v['file']}:{v['line']}` | {v['code'][:60]}... |\n"
            for i, v in enumerate(vulnerabilities, 1)
        )

    @staticmethod
    def _format_exploit_section(exploit_results: dict) -> str:
        sections = []
        for path, result in exploit_results.items():
            status = "✅ 成功" if result.get("success") else "❌ 失敗"
            sec = f"### `{os.path.basename(path)}`\n\n**狀態**: {status}\n\n"
            if result.get("output"):
                flag_lines = [
                    line.strip() for line in result["output"].split("\n")
                    if line.strip() and ("flag" in line.lower() or "HITCON" in line or "LOCAL_TEST" in line)
                ]
                if flag_lines:
                    sec += "```\n" + "\n".join(flag_lines) + "\n```\n\n"
            sections.append(sec)
        return "".join(sections)

    def generate_writeup(self, record: RunRecord) -> Path:
        """Auto-generate a writeup markdown file for a completed run."""
        safe_name = record.package_name.replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        total_vulns = len(record.vulnerabilities)
        high_vulns = sum(1 for v in record.vulnerabilities if v.get("severity") == "high")
        exploits_generated = len(record.exploits_generated)
        exploits_working = sum(1 for r in record.exploit_results.values() if r.get("success"))
        submitted = record.submission_result is not None

        vuln_rows = self._format_vuln_rows(record.vulnerabilities)
        exploit_section = self._format_exploit_section(record.exploit_results)

        writeup = f"""# {record.package_name} {record.package_version} (PHP {record.php_version})

> Auto-generated by Wargame Bot — {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 概覽

| 項目 | 數值 |
|------|------|
| 漏洞總數 | {total_vulns} |
| 高危漏洞 | {high_vulns} |
| 產生 exploit | {exploits_generated} |
| 成功 exploit | {exploits_working} |
| 已提交 | {'是' if submitted else '否'} |

## 漏洞列表

| # | 類型 | 嚴重性 | 位置 | 程式碼 |
|---|------|--------|------|--------|
{vuln_rows}

## Exploit 結果

{exploit_section}
"""

        writeup_path = self.writeups_dir / f"{safe_name}_{timestamp}.md"
        writeup_path.write_text(writeup, encoding="utf-8")
        print(f"[+] Writeup saved: {writeup_path}")
        return writeup_path

    def get_stats(self) -> Dict[str, Any]:
        """Get overall storage statistics."""
        total_runs = 0
        total_submissions = 0
        if self.history_file.exists():
            for line in self.history_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    total_runs += 1
                    record = json.loads(line)
                    if record.get("submission_result"):
                        total_submissions += 1
        return {
            "total_runs": total_runs,
            "total_submissions": total_submissions,
        }
