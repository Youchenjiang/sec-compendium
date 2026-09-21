"""
HITCON 2026 Wargame Bot - Browser Login Helper
Uses Playwright to solve Turnstile CAPTCHA and extract session cookies.
"""
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "bot"))
from config import BASE_URL, EMAIL, PASSWORD


COOKIES_FILE = Path(__file__).parent / ".cookies.json"


def get_cookies(email: str = None, password: str = None, headless: bool = False, refresh: bool = False) -> dict:
    """
    Get session cookies. Returns cached cookies if available, or launches browser login.
    """
    if not refresh and COOKIES_FILE.exists():
        try:
            cached = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
            if cached and isinstance(cached, dict):
                return cached
        except Exception:
            pass
    return browser_login(email=email, password=password, headless=headless)


def browser_login(email: str = None, password: str = None, headless: bool = False) -> dict:
    """
    Login via browser to solve Turnstile CAPTCHA.
    Returns cookies dict for use with requests session.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] playwright not installed: pip install playwright")
        return {}

    email = email or EMAIL
    password = password or PASSWORD

    if not email or not password:
        print("[!] Set WARGAME_EMAIL and WARGAME_PASSWORD in .env or environment")
        return {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        print(f"[*] Navigating to {BASE_URL}")
        page.goto(BASE_URL)

        # Wait for login form
        page.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)

        # Fill credentials
        page.fill("input[type='email'], input[name='email']", email)
        page.fill("input[type='password'], input[name='password']", password)

        # Click login
        page.click("button[type='submit']")

        # Wait for navigation (Turnstile may need manual intervention)
        print("[*] Waiting for login... (solve CAPTCHA if needed)")
        page.wait_for_load_state("networkidle", timeout=30000)

        # Extract cookies
        cookies = {}
        for cookie in page.context.cookies():
            cookies[cookie["name"]] = cookie["value"]

        browser.close()

    # Save cookies
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
    print(f"[+] Cookies saved to {COOKIES_FILE}")

    return cookies


def main():
    cookies = browser_login()
    if cookies:
        print(f"[+] Got {len(cookies)} cookies")
    else:
        print("[-] Login failed")


if __name__ == "__main__":
    main()
