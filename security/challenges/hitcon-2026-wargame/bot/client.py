"""
HITCON 2026 Wargame Bot - API Client
Handles authentication, package listing, and exploit submission.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import requests
from config import BASE_URL, API_BASE as _CONFIG_API_BASE, EMAIL, PASSWORD, REQUEST_TIMEOUT

# Normalize API base URL (supports full URL or relative path)
if _CONFIG_API_BASE.startswith("http://") or _CONFIG_API_BASE.startswith("https://"):
    API_URL = _CONFIG_API_BASE.rstrip("/")
else:
    API_URL = f"{BASE_URL.rstrip('/')}/{_CONFIG_API_BASE.lstrip('/')}"


def _get_browser_cookies(email: str, password: str) -> dict:
    """Helper to lazily import browser_login and fetch session cookies."""
    try:
        from browser_login import get_cookies
    except ImportError:
        tools_dir = Path(__file__).resolve().parent.parent / "scripts" / "tools"
        if str(tools_dir) not in sys.path:
            sys.path.insert(0, str(tools_dir))
        try:
            from browser_login import get_cookies
        except ImportError:
            return {}
    try:
        return get_cookies(email=email, password=password)
    except Exception as e:
        print(f"[*] Browser login unavailable ({e}), falling back to direct API")
        return {}


class WargameClient:
    def __init__(self, email: str = None, password: str = None):
        self.email = email or EMAIL
        self.password = password or PASSWORD
        self.session = requests.Session()
        self.csrf_token = None
        self.authenticated = False

    def _get_csrf_token(self) -> str:
        """Get CSRF token for API requests."""
        resp = self.session.get(
            f"{API_URL}/auth/csrf-token",
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        self.csrf_token = data.get("csrf_token")
        return self.csrf_token

    def login(self) -> bool:
        """Authenticate with the wargame platform."""
        if not self.email or not self.password:
            print("[!] No credentials provided. Set WARGAME_EMAIL and WARGAME_PASSWORD env vars.")
            return False

        # Try browser-based login first (handles Turnstile CAPTCHA)
        try:
            cookies = _get_browser_cookies(self.email, self.password)
            if cookies:
                for name, value in cookies.items():
                    self.session.cookies.set(name, value)

                # Verify we're logged in
                resp = self.session.get(
                    f"{API_URL}/auth/me",
                    timeout=REQUEST_TIMEOUT
                )
                if resp.status_code == 200:
                    data = resp.json()
                    user = data.get("data", {})
                    print(f"[+] Logged in as {user.get('username', self.email)}")
                    self.authenticated = True
                    return True

            # Fallback: try direct API login (may fail without Turnstile)
            csrf_token = self._get_csrf_token()
            resp = self.session.post(
                f"{API_URL}/auth/login",
                json={
                    "email": self.email,
                    "password": self.password,
                    "turnstile_token": ""
                },
                headers={"X-CSRF-Token": csrf_token},
                timeout=REQUEST_TIMEOUT
            )

            if resp.status_code == 200:
                self.authenticated = True
                print(f"[+] Logged in as {self.email}")
                return True
            else:
                print(f"[-] Login failed: {resp.status_code}")
                return False

        except Exception as e:
            print(f"[-] Login error: {e}")
            return False

    def get_packages(self) -> List[Dict[str, Any]]:
        """Get list of available packages."""
        if not self.authenticated and not self.login():
            return []

        resp = self.session.get(
            f"{API_URL}/packages",
            timeout=REQUEST_TIMEOUT
        )

        if resp.status_code == 200:
            data = resp.json()
            packages = data.get("data", [])
            print(f"[+] Found {len(packages)} packages")
            return packages
        else:
            print(f"[-] Failed to get packages: {resp.status_code}")
            return []

    def submit_exploit(self, package_id: str, exploit_content: str) -> Dict[str, Any]:
        """Submit an exploit for a package."""
        if not self.authenticated and not self.login():
            return {"error": "Not authenticated"}

        csrf_token = self._get_csrf_token()

        resp = self.session.post(
            f"{API_URL}/submissions",
            data={
                "package_id": package_id,
                "exploit": exploit_content
            },
            headers={"X-CSRF-Token": csrf_token},
            timeout=REQUEST_TIMEOUT
        )

        if resp.status_code in {200, 201}:
            result = resp.json()
            print(f"[+] Submitted exploit for package {package_id}")
            return result
        else:
            print(f"[-] Submission failed: {resp.status_code}")
            return {"error": resp.text}

    def get_submission_status(self, submission_id: str) -> Dict[str, Any]:
        """Check submission status."""
        resp = self.session.get(
            f"{API_URL}/submissions/{submission_id}",
            timeout=REQUEST_TIMEOUT
        )

        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.status_code}


def create_client(email: str = None, password: str = None) -> WargameClient:
    """Create and return a wargame client instance."""
    client = WargameClient(email, password)
    return client
