"""
Browser Submit — Playwright-based exploit submission (bypasses Turnstile).
Usage: python browser_submit.py <package_name> <exploit_file>
"""
import json
import sys
import time
from pathlib import Path

from urllib.parse import urlparse
_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "bot"))
from config import BASE_URL, SUBMIT_URL

COOKIES_FILE = Path(__file__).parent / ".cookies.json"


def _load_cookies() -> dict:
    if COOKIES_FILE.exists():
        return json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
    return {}


def browser_submit(package_name: str, exploit_code: str, cookies: dict = None) -> bool:
    """Open browser, fill form with exploit, wait for user to solve CAPTCHA and submit."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] playwright not installed: pip install playwright")
        return False

    cookies = cookies or _load_cookies()
    submit_url = SUBMIT_URL
    netloc = urlparse(BASE_URL).netloc
    cookie_domain = netloc.split(":")[0] if ":" in netloc else netloc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for name, value in cookies.items():
            context.add_cookies([{"name": name, "value": value, "domain": cookie_domain, "path": "/"}])

        page = context.new_page()
        page.goto(submit_url, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # Fill package name and select from dropdown
        print(f"[*] Typing package name: {package_name}")
        pkg_input = page.locator('input[placeholder="vendor/package"]')
        pkg_input.fill(package_name)
        time.sleep(2)
        try:
            option = page.locator(f'button:has-text("{package_name}")').first
            option.click()
            time.sleep(2)
            print("[+] Package selected")
        except Exception:
            print("[-] Could not select package from dropdown — fill manually")

        # Fill exploit code
        print("[*] Filling exploit code...")
        textarea = page.locator("textarea").first
        textarea.fill(exploit_code)
        time.sleep(1)

        print()
        print("=" * 50)
        print(" Browser is ready! Please:")
        print("   1. Solve the Turnstile CAPTCHA")
        print("   2. Click 'Create submission'")
        print("   3. Wait for the result")
        print("   4. Close the browser")
        print("=" * 50)
        print()

        try:
            page.wait_for_event("close", timeout=600000)
        except Exception:
            pass
        browser.close()
        print("[+] Done")

    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <package_name> <exploit_file>")
        sys.exit(1)
    pkg = sys.argv[1]
    code = Path(sys.argv[2]).read_text(encoding="utf-8")
    browser_submit(pkg, code)