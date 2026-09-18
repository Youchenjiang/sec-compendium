"""
Output helpers for saving scan results to JSON files.
"""
import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

from .paths import RESULTS_DIR, ensure_dir


def save_json(data: Any, path: Path, indent: int = 2) -> Path:
    """Save data as JSON to the given path, creating parent dirs."""
    ensure_dir(path.parent)
    path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def save_findings(
    findings: List[Dict[str, Any]],
    name: str,
    output_dir: Path = None,
) -> Path:
    """
    Save a list of findings to a timestamped JSON file in results/.

    Args:
        findings: List of finding dicts
        name: Base filename (e.g., "deep_scan")
        output_dir: Override output directory (default: code_auditor/results/)
    """
    if output_dir is None:
        output_dir = RESULTS_DIR

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.json"
    return save_json(findings, output_dir / filename)


def save_summary(
    summary: Dict[str, Any],
    name: str,
    output_dir: Path = None,
) -> Path:
    """Save a summary dict (no timestamp in filename)."""
    if output_dir is None:
        output_dir = RESULTS_DIR
    return save_json(summary, output_dir / f"{name}.json")


def print_finding(finding: Dict[str, Any], prefix: str = "    ") -> None:
    """Pretty-print a single finding."""
    sev = finding.get("severity", "?")
    ftype = finding.get("type", "?")
    ffile = finding.get("file", "?")
    line = finding.get("line", "?")
    code = finding.get("code", "")
    print(f"{prefix}[{sev}] {ftype} in {ffile}:{line}")
    if code:
        print(f"{prefix}  Code: {code[:80]}")


def print_summary_header(title: str) -> None:
    """Print a formatted summary header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_summary_stats(
    total: int,
    by_severity: Dict[str, int] = None,
    extra: Dict[str, Any] = None,
) -> None:
    """Print summary statistics."""
    print(f"  Total findings: {total}")
    if by_severity:
        for sev, count in sorted(by_severity.items()):
            print(f"    {sev}: {count}")
    if extra:
        for k, v in extra.items():
            print(f"  {k}: {v}")
