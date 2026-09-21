"""
HITCON 2026 Wargame Bot - Configuration
"""
import os
from pathlib import Path


# Load .env file if it exists
def _load_env():
    env_path = Path(__file__).parent / ".env"
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

# Wargame platform configuration
BASE_URL = os.getenv("WARGAME_BASE_URL", "https://wargame.d3vc0r3.tw").rstrip("/")
API_BASE = os.getenv("WARGAME_API_BASE", f"{BASE_URL}/api/v1")
SUBMIT_URL = os.getenv("WARGAME_SUBMIT_URL", f"{BASE_URL}/submit")

# Authentication (set via .env or environment variables)
EMAIL = os.getenv("WARGAME_EMAIL", "")
PASSWORD = os.getenv("WARGAME_PASSWORD", "")

# Dist directory (where you extracted the wargame dist)
DIST_DIR = os.getenv("WARGAME_DIST_DIR", "")

# Docker settings
CHALLENGE_PHP_VERSIONS = ["7.4.33", "8.4"]

# Exploit output directory
EXPLOIT_DIR = os.getenv("WARGAME_EXPLOIT_DIR", "")

# Submission cooldown (seconds)
SUBMISSION_COOLDOWN = 60

# Request timeout
REQUEST_TIMEOUT = 30
