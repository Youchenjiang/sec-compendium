"""
Browser automation helper for Cloudflare Turnstile bypass and submission.
"""
import os
import json
import time
from pathlib import Path
from urllib.parse import urlparse
from ..config import PLATFORM_BASE_URL

COOKIES_FILE = Path(__file__).parent / ".cookies.json"


def _normalize_key(url: str, email: str = None) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.split(":")[0].lower() if parsed.netloc else "default"
    account = email.strip().lower() if email else "anonymous"
    return f"{domain}#{account}"


def get_cookies(
    base_url: str = None,
    email: str = None,
    password: str = None,
    headless: bool = False,
    refresh: bool = False,
) -> dict:
    """Get session cookies from domain-scoped cache or via browser login."""
    target_url = base_url or PLATFORM_BASE_URL
    cache_key = _normalize_key(target_url, email)
    if not refresh and COOKIES_FILE.exists():
        try:
            cache = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
            if isinstance(cache, dict) and cache_key in cache:
                cached = cache[cache_key]
                if isinstance(cached, dict):
                    return cached
        except Exception:
            pass

    return browser_login(base_url=target_url, email=email, password=password, headless=headless)


def _save_cookies(cookies: dict, target_url: str, email: str) -> None:
    """Save extracted cookies to persistent local cache file."""
    if not cookies:
        return
    cache = {}
    if COOKIES_FILE.exists():
        try:
            loaded = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                cache = loaded
        except Exception:
            cache = {}

    cache_key = _normalize_key(target_url, email)
    cache[cache_key] = cookies
    COOKIES_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    try:
        os.chmod(COOKIES_FILE, 0o600)  # skipcq: PTC-W6004
    except Exception:
        pass
    print(f"[+] Cookies saved for {cache_key} to {COOKIES_FILE}")


def browser_login(
    base_url: str = None,
    email: str = None,
    password: str = None,
    headless: bool = False,
) -> dict:
    """Login via Playwright browser to solve Turnstile CAPTCHA."""
    target_url = base_url or PLATFORM_BASE_URL
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] playwright not installed: pip install playwright && playwright install chromium")
        return {}

    if not email or not password:
        print("[!] Missing credentials for browser login")
        return {}

    cookies = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        print(f"[*] Navigating to {target_url}")
        page.goto(target_url)

        try:
            page.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)
            page.fill("input[type='email'], input[name='email']", email)
            page.fill("input[type='password'], input[name='password']", password)
            page.click("button[type='submit']")
            print("[*] Waiting for login... (solve CAPTCHA if prompted)")
            page.wait_for_load_state("networkidle", timeout=30000)

            for cookie in page.context.cookies():
                cookies[cookie["name"]] = cookie["value"]
        except Exception as e:
            print(f"[-] Browser login exception: {e}")
        finally:
            browser.close()

    _save_cookies(cookies, target_url, email)
    return cookies


def browser_submit(
    submit_url: str,
    base_url: str,
    package_name: str,
    exploit_code: str,
    cookies: dict = None,
) -> bool:
    """Interactive browser submission fallback for CAPTCHA forms."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] playwright not installed: pip install playwright")
        return False

    cookies = cookies or get_cookies(base_url=base_url)
    netloc = urlparse(base_url).netloc
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

        print(f"[*] Typing target: {package_name}")
        pkg_input = page.locator('input[placeholder="vendor/package"]')
        pkg_input.fill(package_name)
        time.sleep(2)
        try:
            option = page.locator(f'button:has-text("{package_name}")').first
            option.click()
            time.sleep(2)
        except Exception:
            pass

        print("[*] Filling exploit code...")
        textarea = page.locator("textarea").first
        textarea.fill(exploit_code)
        time.sleep(1)

        print("\n" + "=" * 50)
        print(" Browser is ready: solve Turnstile CAPTCHA and submit")
        print("=" * 50 + "\n")

        try:
            page.wait_for_event("close", timeout=600000)
        except Exception:
            pass
        browser.close()

    return True
