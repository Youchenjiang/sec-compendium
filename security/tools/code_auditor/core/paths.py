"""
Centralized path resolution for Code Auditor.
"""
from pathlib import Path
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOOL_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = Path(os.getenv('AUDIT_RESULTS_DIR', str(TOOL_ROOT / 'results')))
REPORTS_DIR = RESULTS_DIR / 'reports'
EXPLOITS_DIR = RESULTS_DIR / 'exploits'
WRITEUPS_DIR = RESULTS_DIR / 'writeups'
LOGS_DIR = RESULTS_DIR / 'logs'


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
