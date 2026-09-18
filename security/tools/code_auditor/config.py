"""
Code Auditor - Central Configuration & Environment Manager
"""
import os
from pathlib import Path


def _load_env():
    candidates = [
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent.parent.parent / ".env",
    ]
    for env_path in candidates:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value:
                        os.environ.setdefault(key, value)


_load_env()

# Platform and target configuration
PLATFORM_BASE_URL = os.getenv("WARGAME_BASE_URL", os.getenv("AUDITOR_BASE_URL", "https://wargame.d3vc0r3.tw")).rstrip("/")
PLATFORM_API_BASE = os.getenv("WARGAME_API_BASE", os.getenv("AUDITOR_API_BASE", f"{PLATFORM_BASE_URL}/api/v1"))
PLATFORM_SUBMIT_URL = os.getenv("WARGAME_SUBMIT_URL", os.getenv("AUDITOR_SUBMIT_URL", f"{PLATFORM_BASE_URL}/submit"))

# Credentials
EMAIL = os.getenv("WARGAME_EMAIL", os.getenv("AUDITOR_EMAIL", ""))
PASSWORD = os.getenv("WARGAME_PASSWORD", os.getenv("AUDITOR_PASSWORD", ""))

# Source code and dist paths
DIST_DIR = os.getenv("WARGAME_DIST_DIR", os.getenv("AUDITOR_DIST_DIR", ""))
EXPLOIT_DIR = os.getenv("WARGAME_EXPLOIT_DIR", os.getenv("AUDITOR_EXPLOIT_DIR", ""))

# Docker environments
CHALLENGE_PHP_VERSIONS = ["7.4.33", "8.4"]
SUBMISSION_COOLDOWN = 60
REQUEST_TIMEOUT = 30
