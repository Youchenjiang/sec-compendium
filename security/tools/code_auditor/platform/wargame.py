"""
REST API Platform Client for CTF & Wargame Platforms.
"""
from typing import Dict, Any, List
import requests
from .base import BasePlatformClient
from .browser_helper import get_cookies
from ..config import PLATFORM_BASE_URL


class WargamePlatformClient(BasePlatformClient):
    """Client for REST-based CTF/Wargame platforms."""

    def __init__(
        self,
        base_url: str = None,
        api_base: str = None,
        email: str = None,
        password: str = None,
        timeout: int = 30,
    ):
        self.base_url = (base_url or PLATFORM_BASE_URL).rstrip("/")
        api_prefix = api_base or f"{self.base_url}/api/v1"
        if api_prefix.startswith("http://") or api_prefix.startswith("https://"):
            self.api_url = api_prefix.rstrip("/")
        else:
            self.api_url = f"{self.base_url}/{api_prefix.lstrip('/')}"

        self.email = email or ""
        self.password = password or ""
        self.timeout = timeout
        self.session = requests.Session()
        self.csrf_token = None
        self.authenticated = False

    def _get_csrf_token(self) -> str:
        resp = self.session.get(f"{self.api_url}/auth/csrf-token", timeout=self.timeout)
        resp.raise_for_status()
        self.csrf_token = resp.json().get("csrf_token")
        return self.csrf_token

    def login(self) -> bool:
        if not self.email or not self.password:
            print("[!] No credentials provided for platform login.")
            return False

        # 1. Try browser cookies (handles Turnstile)
        try:
            cookies = get_cookies(base_url=self.base_url, email=self.email, password=self.password)
            if cookies:
                for name, value in cookies.items():
                    self.session.cookies.set(name, value)
                resp = self.session.get(f"{self.api_url}/auth/me", timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    user = data.get("data", {})
                    print(f"[+] Logged in as {user.get('username', self.email)}")
                    self.authenticated = True
                    return True
        except Exception as e:
            print(f"[*] Browser cookie login fallback: {e}")

        # 2. Direct API login fallback
        try:
            csrf = self._get_csrf_token()
            resp = self.session.post(
                f"{self.api_url}/auth/login",
                json={"email": self.email, "password": self.password, "turnstile_token": ""},
                headers={"X-CSRF-Token": csrf},
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                self.authenticated = True
                print(f"[+] Logged in directly via API as {self.email}")
                return True
            else:
                print(f"[-] Platform login failed: {resp.status_code}")
                return False
        except Exception as e:
            print(f"[-] Login error: {e}")
            return False

    def get_targets(self) -> List[Dict[str, Any]]:
        if not self.authenticated and not self.login():
            return []

        resp = self.session.get(f"{self.api_url}/packages", timeout=self.timeout)
        if resp.status_code == 200:
            packages = resp.json().get("data", [])
            print(f"[+] Discovered {len(packages)} targets on platform")
            return packages
        return []

    def submit(self, target_id: str, exploit_content: str) -> Dict[str, Any]:
        if not self.authenticated and not self.login():
            return {"error": "Not authenticated"}

        csrf = self._get_csrf_token()
        resp = self.session.post(
            f"{self.api_url}/submissions",
            data={"package_id": target_id, "exploit": exploit_content},
            headers={"X-CSRF-Token": csrf},
            timeout=self.timeout,
        )
        if resp.status_code in (200, 201):
            return resp.json()
        return {"error": resp.text, "status_code": resp.status_code}

    def get_status(self, submission_id: str) -> Dict[str, Any]:
        resp = self.session.get(f"{self.api_url}/submissions/{submission_id}", timeout=self.timeout)
        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.status_code}
